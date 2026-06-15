<?php
/**
 * 订单 API
 * 
 * GET                      - 获取当前用户订单历史
 * GET ?order_id=xxx        - 获取订单详情
 * POST action=create         - 创建订单
 * POST action=update_delivery - 更新订单配送信息
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

// 初始化订单表
initOrderTables();

$method = $_SERVER['REQUEST_METHOD'];
$action = isset($_GET['action']) ? $_GET['action'] : '';

if ($method === 'GET' && $action !== 'create') {
    if (isset($_GET['order_id'])) {
        handleGetOrderDetail();
    } else {
        handleGetOrders();
    }
} elseif ($method === 'POST' && $action === 'create') {
    handleCreateOrder();
} elseif ($method === 'POST' && $action === 'update_delivery') {
    handleUpdateDelivery();
} else {
    errorResponse('未知操作');
}

function initOrderTables() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        order_number VARCHAR(20) NOT NULL,
        delivery_type ENUM('pickup', 'delivery') NOT NULL DEFAULT 'pickup',
        delivery_villager VARCHAR(50) DEFAULT NULL,
        delivery_address VARCHAR(255) DEFAULT NULL,
        total_items INT NOT NULL DEFAULT 0,
        total_price INT NOT NULL DEFAULT 0,
        total_loves INT NOT NULL DEFAULT 0,
        total_hates INT NOT NULL DEFAULT 0,
        status ENUM('pending', 'confirmed', 'delivered') NOT NULL DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_order_number (order_number)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
    
    $conn->query("CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        item_id VARCHAR(50) NOT NULL,
        item_name VARCHAR(100) NOT NULL,
        quality VARCHAR(20) DEFAULT '',
        quantity INT NOT NULL DEFAULT 1,
        price INT NOT NULL DEFAULT 0,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetOrders() {
    $user = requireLogin();
    
    $conn = getDB();
    $stmt = $conn->prepare("SELECT id, order_number, delivery_type, delivery_villager, delivery_address, total_items, total_price, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $orders = [];
    while ($row = $result->fetch_assoc()) {
        $orderId = (int)$row['id'];
        // 加载每个订单的商品列表
        $itemStmt = $conn->prepare("SELECT item_id, item_name, quality, quantity, price FROM order_items WHERE order_id = ?");
        $itemStmt->bind_param("i", $orderId);
        $itemStmt->execute();
        $itemResult = $itemStmt->get_result();
        $items = [];
        while ($itemRow = $itemResult->fetch_assoc()) {
            $items[] = [
                'item_id' => $itemRow['item_id'],
                'item_name' => $itemRow['item_name'],
                'quality' => $itemRow['quality'],
                'quantity' => (int)$itemRow['quantity'],
                'price' => (int)$itemRow['price']
            ];
        }
        $itemStmt->close();
        
        $orders[] = [
            'id' => $orderId,
            'order_number' => $row['order_number'],
            'delivery_type' => $row['delivery_type'],
            'delivery_villager' => $row['delivery_villager'],
            'delivery_address' => $row['delivery_address'],
            'total_items' => (int)$row['total_items'],
            'total_price' => (int)$row['total_price'],
            'status' => $row['status'],
            'created_at' => $row['created_at'],
            'items' => $items
        ];
    }
    $stmt->close();
    
    successResponse('获取成功', ['orders' => $orders]);
}

function handleGetOrderDetail() {
    $user = requireLogin();
    $orderId = (int)($_GET['order_id'] ?? 0);
    
    if ($orderId <= 0) errorResponse('无效的订单ID');
    
    $conn = getDB();
    
    // 获取订单信息
    $stmt = $conn->prepare("SELECT * FROM orders WHERE id = ? AND user_id = ?");
    $stmt->bind_param("ii", $orderId, $user['id']);
    $stmt->execute();
    $order = $stmt->get_result()->fetch_assoc();
    $stmt->close();
    
    if (!$order) errorResponse('订单不存在');
    
    // 获取订单商品
    $stmt = $conn->prepare("SELECT * FROM order_items WHERE order_id = ?");
    $stmt->bind_param("i", $orderId);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $items = [];
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'item_id' => $row['item_id'],
            'item_name' => $row['item_name'],
            'quality' => $row['quality'],
            'quantity' => (int)$row['quantity'],
            'price' => (int)$row['price']
        ];
    }
    $stmt->close();
    
    successResponse('获取成功', [
        'order' => [
            'id' => (int)$order['id'],
            'order_number' => $order['order_number'],
            'delivery_type' => $order['delivery_type'],
            'delivery_villager' => $order['delivery_villager'],
            'delivery_address' => $order['delivery_address'],
            'total_items' => (int)$order['total_items'],
            'total_price' => (int)$order['total_price'],
            'total_loves' => (int)$order['total_loves'],
            'total_hates' => (int)$order['total_hates'],
            'status' => $order['status'],
            'created_at' => $order['created_at']
        ],
        'items' => $items
    ]);
}

function handleCreateOrder() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $deliveryType = $input['delivery_type'] ?? 'pickup';
    $deliveryVillager = $input['delivery_villager'] ?? null;
    $deliveryAddress = $input['delivery_address'] ?? null;
    $orderItems = $input['items'] ?? [];
    
    if (!in_array($deliveryType, ['pickup', 'delivery'])) {
        errorResponse('无效的配送类型');
    }
    
    if (empty($orderItems)) {
        errorResponse('订单商品不能为空');
    }
    
    // 获取物品数据文件（用于查价格和名称）
    $itemsDataFile = realpath(__DIR__ . '/../items_data.js');
    $itemsMap = [];
    if ($itemsDataFile && file_exists($itemsDataFile)) {
        $jsContent = file_get_contents($itemsDataFile);
        // 提取 JSON 数组：items_data.js 格式为 window.ITEMS_DATA = [...]
        if (preg_match('/window\.ITEMS_DATA\s*=\s*(\[.*\]);/s', $jsContent, $m)) {
            $itemsArr = json_decode($m[1], true);
            if (is_array($itemsArr)) {
                foreach ($itemsArr as $item) {
                    $itemsMap[$item['id']] = $item;
                }
            }
        }
    }
    
    $conn = getDB();
    $conn->begin_transaction();
    
    try {
        // 生成订单号
        $orderNumber = generateOrderNumber($conn);
        
        // 计算总计（从数据库/JS文件查价格，不依赖前端传值）
        $totalItems = 0;
        $totalPrice = 0;
        $totalLoves = 0;
        $totalHates = 0;
        
        // 前端直接传递商品名称、价格、喜爱/讨厌数
        $resolvedItems = [];
        foreach ($orderItems as $item) {
            $itemId = $item['item_id'] ?? '';
            $itemName = $item['name'] ?? $itemId;
            $quality = $item['quality'] ?? '';
            $quantity = max(1, intval($item['quantity'] ?? 1));
            $price = intval($item['price'] ?? 0);
            $loveCount = intval($item['loves'] ?? 0);
            $hateCount = intval($item['hates'] ?? 0);
            
            $totalItems += $quantity;
            $totalPrice += $price * $quantity;
            $totalLoves += $loveCount * $quantity;
            $totalHates += $hateCount * $quantity;
            
            $resolvedItems[] = [
                'item_id' => $itemId,
                'item_name' => $itemName,
                'quality' => $quality,
                'quantity' => $quantity,
                'price' => $price
            ];
        }
        
        // 插入订单
        $stmt = $conn->prepare("INSERT INTO orders (user_id, order_number, delivery_type, delivery_villager, delivery_address, total_items, total_price, total_loves, total_hates, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'confirmed')");
        $stmt->bind_param("issssiiii", $user['id'], $orderNumber, $deliveryType, $deliveryVillager, $deliveryAddress, $totalItems, $totalPrice, $totalLoves, $totalHates);
        $stmt->execute();
        $orderId = $conn->insert_id;
        $stmt->close();
        
        // 插入订单商品
        $stmt = $conn->prepare("INSERT INTO order_items (order_id, item_id, item_name, quality, quantity, price) VALUES (?, ?, ?, ?, ?, ?)");
        foreach ($resolvedItems as $ri) {
            $stmt->bind_param("isssii", 
                $orderId, 
                $ri['item_id'], 
                $ri['item_name'], 
                $ri['quality'], 
                $ri['quantity'], 
                $ri['price']
            );
            $stmt->execute();
        }
        $stmt->close();
        
        // 清空购物车（如果购物车结账的话）
        if (!empty($input['clear_cart'])) {
            $stmt = $conn->prepare("DELETE FROM cart_items WHERE user_id = ?");
            $stmt->bind_param("i", $user['id']);
            $stmt->execute();
            $stmt->close();
        }
        
        $conn->commit();
        
        successResponse('订单创建成功', [
            'order_id' => $orderId,
            'order_number' => $orderNumber
        ]);
        
    } catch (Exception $e) {
        $conn->rollback();
        errorResponse('订单创建失败: ' . $e->getMessage());
    }
}

function generateOrderNumber($conn) {
    $chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $prefix = 'ORD';
    
    do {
        $suffix = '';
        for ($i = 0; $i < 10; $i++) {
            $suffix .= $chars[random_int(0, strlen($chars) - 1)];
        }
        $orderNumber = $prefix . $suffix;
        
        // 检查是否已存在
        $stmt = $conn->prepare("SELECT id FROM orders WHERE order_number = ?");
        $stmt->bind_param("s", $orderNumber);
        $stmt->execute();
        $exists = $stmt->get_result()->num_rows > 0;
        $stmt->close();
    } while ($exists);
    
    return $orderNumber;
}

function handleUpdateDelivery() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $orderId = intval($input['order_id'] ?? 0);
    $deliveryType = $input['delivery_type'] ?? 'pickup';
    $deliveryVillager = $input['delivery_villager'] ?? null;
    $deliveryAddress = $input['delivery_address'] ?? null;
    
    if ($orderId <= 0) errorResponse('无效的订单ID');
    if (!in_array($deliveryType, ['pickup', 'delivery', 'pending'])) {
        errorResponse('无效的配送类型');
    }
    
    $conn = getDB();
    
    // 验证订单属于当前用户
    $stmt = $conn->prepare("SELECT id FROM orders WHERE id = ? AND user_id = ?");
    $stmt->bind_param("ii", $orderId, $user['id']);
    $stmt->execute();
    if ($stmt->get_result()->num_rows === 0) {
        $stmt->close();
        errorResponse('订单不存在');
    }
    $stmt->close();
    
    // 更新配送信息
    $stmt = $conn->prepare("UPDATE orders SET delivery_type = ?, delivery_villager = ?, delivery_address = ? WHERE id = ?");
    $stmt->bind_param("sssi", $deliveryType, $deliveryVillager, $deliveryAddress, $orderId);
    $stmt->execute();
    $stmt->close();
    
    successResponse('配送信息更新成功', ['order_id' => $orderId]);
}
?>
