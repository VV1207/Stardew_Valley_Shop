<?php
/**
 * 订单评价 API
 * 
 * GET                           - 获取当前用户所有评价
 * GET ?order_id=xxx             - 获取某个订单的评价
 * POST action=create            - 创建评价
 * POST action=update            - 修改评价
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

// 初始化评价表
initReviewTable();

$method = $_SERVER['REQUEST_METHOD'];
$action = isset($_GET['action']) ? $_GET['action'] : '';

if ($method === 'GET') {
    if (isset($_GET['order_id'])) {
        handleGetReviewByOrder();
    } else {
        handleGetReviews();
    }
} elseif ($method === 'POST' && $action === 'create') {
    handleCreateReview();
} elseif ($method === 'POST' && $action === 'update') {
    handleUpdateReview();
} else {
    errorResponse('未知操作');
}

function initReviewTable() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS order_reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        order_id INT NOT NULL,
        delivery_rating TINYINT NOT NULL DEFAULT 5,
        quality_rating TINYINT NOT NULL DEFAULT 5,
        overall_rating TINYINT NOT NULL DEFAULT 5,
        comment TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        UNIQUE KEY unique_user_order (user_id, order_id),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetReviews() {
    $user = requireLogin();
    $conn = getDB();
    
    $stmt = $conn->prepare("SELECT r.*, o.order_number FROM order_reviews r JOIN orders o ON r.order_id = o.id WHERE r.user_id = ? ORDER BY r.created_at DESC");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $reviews = [];
    while ($row = $result->fetch_assoc()) {
        $reviews[] = [
            'id' => (int)$row['id'],
            'order_id' => (int)$row['order_id'],
            'order_number' => $row['order_number'],
            'delivery_rating' => (int)$row['delivery_rating'],
            'quality_rating' => (int)$row['quality_rating'],
            'overall_rating' => (int)$row['overall_rating'],
            'comment' => $row['comment'],
            'created_at' => $row['created_at'],
            'updated_at' => $row['updated_at']
        ];
    }
    $stmt->close();
    
    successResponse('获取成功', ['reviews' => $reviews]);
}

function handleGetReviewByOrder() {
    $user = requireLogin();
    $orderId = intval($_GET['order_id']);
    
    if ($orderId <= 0) errorResponse('无效的订单ID');
    
    $conn = getDB();
    $stmt = $conn->prepare("SELECT * FROM order_reviews WHERE user_id = ? AND order_id = ?");
    $stmt->bind_param("ii", $user['id'], $orderId);
    $stmt->execute();
    $result = $stmt->get_result();
    $stmt->close();
    
    if ($row = $result->fetch_assoc()) {
        successResponse('获取成功', ['review' => [
            'id' => (int)$row['id'],
            'order_id' => (int)$row['order_id'],
            'delivery_rating' => (int)$row['delivery_rating'],
            'quality_rating' => (int)$row['quality_rating'],
            'overall_rating' => (int)$row['overall_rating'],
            'comment' => $row['comment'],
            'created_at' => $row['created_at'],
            'updated_at' => $row['updated_at']
        ]]);
    } else {
        successResponse('暂无评价', ['review' => null]);
    }
}

function handleCreateReview() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $orderId = intval($input['order_id'] ?? 0);
    $deliveryRating = intval($input['delivery_rating'] ?? 0);
    $qualityRating = intval($input['quality_rating'] ?? 0);
    $overallRating = intval($input['overall_rating'] ?? 0);
    $comment = trim($input['comment'] ?? '');
    
    if ($orderId <= 0) errorResponse('无效的订单ID');
    if ($deliveryRating < 1 || $deliveryRating > 5) errorResponse('收货服务评分需在1-5之间');
    if ($qualityRating < 1 || $qualityRating > 5) errorResponse('商品品质评分需在1-5之间');
    if ($overallRating < 1 || $overallRating > 5) errorResponse('综合评分需在1-5之间');
    
    $conn = getDB();
    
    // 验证订单属于当前用户
    $stmt = $conn->prepare("SELECT id FROM orders WHERE id = ? AND user_id = ?");
    $stmt->bind_param("ii", $orderId, $user['id']);
    $stmt->execute();
    if ($stmt->get_result()->num_rows === 0) {
        $stmt->close();
        errorResponse('订单不存在或无权评价');
    }
    $stmt->close();
    
    // 检查是否已有评价
    $stmt = $conn->prepare("SELECT id FROM order_reviews WHERE user_id = ? AND order_id = ?");
    $stmt->bind_param("ii", $user['id'], $orderId);
    $stmt->execute();
    if ($stmt->get_result()->num_rows > 0) {
        $stmt->close();
        errorResponse('该订单已评价，请使用update修改');
    }
    $stmt->close();
    
    // 插入评价
    $stmt = $conn->prepare("INSERT INTO order_reviews (user_id, order_id, delivery_rating, quality_rating, overall_rating, comment) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("iiiiis", $user['id'], $orderId, $deliveryRating, $qualityRating, $overallRating, $comment);
    $stmt->execute();
    $reviewId = $conn->insert_id;
    $stmt->close();
    
    successResponse('评价提交成功', ['review_id' => $reviewId]);
}

function handleUpdateReview() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $orderId = intval($input['order_id'] ?? 0);
    $deliveryRating = intval($input['delivery_rating'] ?? 0);
    $qualityRating = intval($input['quality_rating'] ?? 0);
    $overallRating = intval($input['overall_rating'] ?? 0);
    $comment = trim($input['comment'] ?? '');
    
    if ($orderId <= 0) errorResponse('无效的订单ID');
    if ($deliveryRating < 1 || $deliveryRating > 5) errorResponse('收货服务评分需在1-5之间');
    if ($qualityRating < 1 || $qualityRating > 5) errorResponse('商品品质评分需在1-5之间');
    if ($overallRating < 1 || $overallRating > 5) errorResponse('综合评分需在1-5之间');
    
    $conn = getDB();
    
    // 更新评价
    $stmt = $conn->prepare("UPDATE order_reviews SET delivery_rating = ?, quality_rating = ?, overall_rating = ?, comment = ? WHERE user_id = ? AND order_id = ?");
    $stmt->bind_param("iiisii", $deliveryRating, $qualityRating, $overallRating, $comment, $user['id'], $orderId);
    $stmt->execute();
    
    if ($stmt->affected_rows > 0) {
        successResponse('评价修改成功');
    } else {
        errorResponse('评价不存在或无权修改');
    }
    $stmt->close();
}
?>