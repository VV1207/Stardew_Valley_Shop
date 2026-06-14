<?php
/**
 * 收藏 API
 * 
 * GET  /api/favorites.php              - 获取收藏列表
 * POST /api/favorites.php?action=toggle - 切换收藏状态
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

$action = isset($_GET['action']) ? $_GET['action'] : '';

// 初始化收藏表
initFavoritesTable();

switch ($action) {
    case 'toggle':
        handleToggle();
        break;
    default:
        handleGetFavorites();
}

function initFavoritesTable() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS favorites (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        item_id VARCHAR(50) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_user_item (user_id, item_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetFavorites() {
    $user = getCurrentUser();
    if (!$user) {
        successResponse('未登录', ['favorites' => []]);
        return;
    }
    
    $conn = getDB();
    $stmt = $conn->prepare("SELECT item_id FROM favorites WHERE user_id = ? ORDER BY created_at DESC");
    $stmt->bind_param("i", $user['id']);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $favorites = [];
    while ($row = $result->fetch_assoc()) {
        $favorites[] = $row['item_id'];
    }
    $stmt->close();
    
    successResponse('获取成功', ['favorites' => $favorites]);
}

function handleToggle() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    $itemId = $input['item_id'] ?? '';
    
    if (empty($itemId)) errorResponse('缺少 item_id');
    
    $conn = getDB();
    
    // 检查是否已收藏
    $stmt = $conn->prepare("SELECT id FROM favorites WHERE user_id = ? AND item_id = ?");
    $stmt->bind_param("is", $user['id'], $itemId);
    $stmt->execute();
    $existing = $stmt->get_result()->fetch_assoc();
    $stmt->close();
    
    if ($existing) {
        // 取消收藏
        $stmt = $conn->prepare("DELETE FROM favorites WHERE user_id = ? AND item_id = ?");
        $stmt->bind_param("is", $user['id'], $itemId);
        $stmt->execute();
        $stmt->close();
        
        $newFavorited = false;
        successResponse('已取消收藏', ['favorited' => false]);
    } else {
        // 添加收藏
        $stmt = $conn->prepare("INSERT INTO favorites (user_id, item_id) VALUES (?, ?)");
        $stmt->bind_param("is", $user['id'], $itemId);
        $stmt->execute();
        $stmt->close();
        
        successResponse('已收藏', ['favorited' => true]);
    }
}
?>