<?php
/**
 * 用户反馈 API
 * 
 * GET                           - 获取所有用户的反馈（含用户名）
 * POST action=create            - 提交反馈
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

// 初始化反馈表
initFeedbackTable();

$method = $_SERVER['REQUEST_METHOD'];
$action = isset($_GET['action']) ? $_GET['action'] : '';

if ($method === 'GET') {
    handleGetAllFeedbacks();
} elseif ($method === 'POST' && $action === 'create') {
    handleCreateFeedback();
} else {
    errorResponse('未知操作');
}

function initFeedbackTable() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS user_feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        type VARCHAR(20) NOT NULL DEFAULT '其他',
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_user_id (user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetAllFeedbacks() {
    $user = requireLogin();
    $conn = getDB();
    
    // 获取所有用户的反馈，JOIN users 表获取用户名
    $stmt = $conn->query("
        SELECT f.id, f.type, f.content, f.created_at, f.user_id, u.username 
        FROM user_feedback f 
        LEFT JOIN users u ON f.user_id = u.id 
        ORDER BY f.created_at DESC
    ");
    
    $feedbacks = [];
    while ($row = $stmt->fetch_assoc()) {
        $feedbacks[] = [
            'id' => (int)$row['id'],
            'type' => $row['type'],
            'content' => $row['content'],
            'username' => $row['username'] ?? '未知用户',
            'user_id' => (int)$row['user_id'],
            'is_self' => ((int)$row['user_id'] === (int)$user['id']),
            'created_at' => $row['created_at']
        ];
    }
    
    successResponse('获取成功', ['feedbacks' => $feedbacks]);
}

function handleCreateFeedback() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    
    $type = trim($input['type'] ?? '其他');
    $content = trim($input['content'] ?? '');
    
    $allowedTypes = ['建议', '问题', '体验', '其他'];
    if (!in_array($type, $allowedTypes)) {
        errorResponse('无效的反馈类型');
    }
    
    if (empty($content)) {
        errorResponse('反馈内容不能为空');
    }
    
    if (mb_strlen($content) > 2000) {
        errorResponse('反馈内容不能超过2000字');
    }
    
    $conn = getDB();
    $stmt = $conn->prepare("INSERT INTO user_feedback (user_id, type, content) VALUES (?, ?, ?)");
    $stmt->bind_param("iss", $user['id'], $type, $content);
    $stmt->execute();
    $feedbackId = $conn->insert_id;
    $stmt->close();
    
    successResponse('反馈提交成功', ['feedback_id' => $feedbackId]);
}
?>