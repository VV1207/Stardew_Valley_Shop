<?php
/**
 * 购物车 API
 * 
 * GET               - 获取购物车
 * POST action=add   - 添加商品
 * POST action=update - 更新数量
 * POST action=remove - 移除商品
 * POST action=clear  - 清空购物车
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

// 初始化购物车表
initCartTable();

// 获取请求方法和动作
$method = $_SERVER['REQUEST_METHOD'];
$action = isset($_POST['action']) ? $_POST['action'] : (isset($_GET['action']) ? $_GET['action'] : '');

if ($method === 'GET') {
    handleGetCart();
} elseif ($method === 'POST') {
    switch ($action) {
        case 'add':
            handleAddItem();
            break;
        case 'update':
            handleUpdateItem();
            break;
        case 'remove':
            handleRemoveItem();
            break;
        case 'clear':
            handleClearCart();
            break;
        default:
            errorResponse('未知操作');
    }
} else {
    errorResponse('不支持的请求方法');
}

function initCartTable() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS cart_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        item_id VARCHAR(50) NOT NULL,
        quality VARCHAR(20) DEFAULT '',
        quantity INT NOT NULL DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_cart_item (user_id, item_id, quality)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetCart() {
    $user = getCurrentUser();
    if (!$user) {
        successResponse('未登录', ['items' => []]);
        return;
    }
    
    $conn = getDB();
    $stmt = $conn->prepare("SELECT item_id, quality, quantity FROM cart_items WHERE user_id = ? ORDER BY created_at ASC");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $items = [];
    while ($row = $result->fetch_assoc()) {
        $items[] = [
            'item_id' => $row['item_id'],
            'quality' => $row['quality'],
            'quantity' => (int)$row['quantity']
        ];
    }
    $stmt->close();
    
    successResponse('获取成功', ['items' => $items]);
}

function handleAddItem() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $itemId = $input['item_id'] ?? '';
    $quality = $input['quality'] ?? '';
    $quantity = isset($input['quantity']) ? (int)$input['quantity'] : 1;
    
    if (empty($itemId)) errorResponse('缺少 item_id');
    if ($quantity <= 0 || $quantity > 999) errorResponse('数量必须在 1-999 之间');
    
    $conn = getDB();
    
    // 检查是否已存在相同商品+品质
    $stmt = $conn->prepare("SELECT id, quantity FROM cart_items WHERE user_id = ? AND item_id = ? AND quality = ?");
    $stmt->bind_param("iss", $user['id'], $itemId, $quality);
    $stmt->execute();
    $existing = $stmt->get_result()->fetch_assoc();
    $stmt->close();
    
    if ($existing) {
        // 更新数量
        $newQty = $existing['quantity'] + $quantity;
        if ($newQty > 999) $newQty = 999;
        $stmt = $conn->prepare("UPDATE cart_items SET quantity = ? WHERE id = ?");
        $stmt->bind_param("ii", $newQty, $existing['id']);
        $stmt->execute();
        $stmt->close();
    } else {
        // 插入新记录
        $stmt = $conn->prepare("INSERT INTO cart_items (user_id, item_id, quality, quantity) VALUES (?, ?, ?, ?)");
        $stmt->bind_param("issi", $user['id'], $itemId, $quality, $quantity);
        $stmt->execute();
        $stmt->close();
    }
    
    successResponse('添加成功');
}

function handleUpdateItem() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $itemId = $input['item_id'] ?? '';
    $quality = $input['quality'] ?? '';
    $quantity = isset($input['quantity']) ? (int)$input['quantity'] : 0;
    
    if (empty($itemId)) errorResponse('缺少 item_id');
    if ($quantity < 0 || $quantity > 999) errorResponse('数量必须在 0-999 之间');
    
    $conn = getDB();
    
    if ($quantity <= 0) {
        // 删除记录
        $stmt = $conn->prepare("DELETE FROM cart_items WHERE user_id = ? AND item_id = ? AND quality = ?");
        $stmt->bind_param("iss", $user['id'], $itemId, $quality);
        $stmt->execute();
        $stmt->close();
    } else {
        // 更新数量
        $stmt = $conn->prepare("UPDATE cart_items SET quantity = ? WHERE user_id = ? AND item_id = ? AND quality = ?");
        $stmt->bind_param("iiss", $quantity, $user['id'], $itemId, $quality);
        $stmt->execute();
        $stmt->close();
    }
    
    successResponse('更新成功');
}

function handleRemoveItem() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $itemId = $input['item_id'] ?? '';
    $quality = $input['quality'] ?? '';
    
    if (empty($itemId)) errorResponse('缺少 item_id');
    
    $conn = getDB();
    $stmt = $conn->prepare("DELETE FROM cart_items WHERE user_id = ? AND item_id = ? AND quality = ?");
    $stmt->bind_param("iss", $user['id'], $itemId, $quality);
    $stmt->execute();
    $stmt->close();
    
    successResponse('移除成功');
}

function handleClearCart() {
    $user = requireLogin();
    
    $conn = getDB();
    $stmt = $conn->prepare("DELETE FROM cart_items WHERE user_id = ?");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $stmt->close();
    
    successResponse('购物车已清空');
}
?>