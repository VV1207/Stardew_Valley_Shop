<?php
/**
 * 新闻互动 API
 * 
 * GET  /api/interact.php?news_id=xxx           - 获取互动数据
 * POST /api/interact.php?action=like            - 点赞/取消点赞
 * POST /api/interact.php?action=comment         - 发表评论
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

$action = isset($_GET['action']) ? $_GET['action'] : '';
$newsId = isset($_GET['news_id']) ? $_GET['news_id'] : '';

// 初始化数据库表
initInteractionTables();

switch ($action) {
    case 'like':
        handleLike();
        break;
    case 'comment':
        handleComment();
        break;
    case 'delete_comment':
        handleDeleteComment();
        break;
    default:
        if ($newsId) {
            handleGetInteraction($newsId);
        } else {
            errorResponse('缺少 news_id 参数');
        }
}

function initInteractionTables() {
    $conn = getDB();
    $conn->query("CREATE TABLE IF NOT EXISTS news_interactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id VARCHAR(50) NOT NULL,
        user_id INT NOT NULL,
        liked TINYINT(1) DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY unique_news_user (news_id, user_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
    $conn->query("CREATE TABLE IF NOT EXISTS news_comments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        news_id VARCHAR(50) NOT NULL,
        user_id INT NOT NULL,
        comment_text TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_news_id (news_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
}

function handleGetInteraction($newsId) {
    $conn = getDB();
    
    // 总点赞数
    $stmt = $conn->prepare("SELECT COUNT(*) as total FROM news_interactions WHERE news_id = ? AND liked = 1");
    $stmt->bind_param("s", $newsId);
    $stmt->execute();
    $totalLikes = $stmt->get_result()->fetch_assoc()['total'];
    $stmt->close();
    
    // 当前用户是否已点赞
    $liked = false;
    $user = getCurrentUser();
    if ($user) {
        $stmt = $conn->prepare("SELECT liked FROM news_interactions WHERE news_id = ? AND user_id = ?");
        $stmt->bind_param("si", $newsId, $user['id']);
        $stmt->execute();
        $result = $stmt->get_result()->fetch_assoc();
        $liked = $result ? (bool)$result['liked'] : false;
        $stmt->close();
    }
    
    // 获取评论
    $stmt = $conn->prepare("SELECT nc.id, nc.comment_text, nc.created_at, u.username 
        FROM news_comments nc 
        JOIN users u ON nc.user_id = u.id 
        WHERE nc.news_id = ? 
        ORDER BY nc.created_at ASC");
    $stmt->bind_param("s", $newsId);
    $stmt->execute();
    $comments = [];
    $result = $stmt->get_result();
    while ($row = $result->fetch_assoc()) {
        $comments[] = [
            'id' => (int)$row['id'],
            'author' => $row['username'],
            'text' => $row['comment_text'],
            'time' => $row['created_at']
        ];
    }
    $stmt->close();
    
    successResponse('获取成功', [
        'news_id' => $newsId,
        'likes' => (int)$totalLikes,
        'liked' => $liked,
        'comments' => $comments
    ]);
}

function handleLike() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    $newsId = $input['news_id'] ?? '';
    
    if (empty($newsId)) errorResponse('缺少 news_id');
    
    $conn = getDB();
    
    // 检查是否已有记录
    $stmt = $conn->prepare("SELECT liked FROM news_interactions WHERE news_id = ? AND user_id = ?");
    $stmt->bind_param("si", $newsId, $user['id']);
    $stmt->execute();
    $existing = $stmt->get_result()->fetch_assoc();
    $stmt->close();
    
    if ($existing) {
        // 切换点赞状态
        $newLiked = $existing['liked'] ? 0 : 1;
        $stmt = $conn->prepare("UPDATE news_interactions SET liked = ? WHERE news_id = ? AND user_id = ?");
        $stmt->bind_param("isi", $newLiked, $newsId, $user['id']);
    } else {
        // 新建记录
        $newLiked = 1;
        $stmt = $conn->prepare("INSERT INTO news_interactions (news_id, user_id, liked) VALUES (?, ?, 1)");
        $stmt->bind_param("si", $newsId, $user['id']);
    }
    $stmt->execute();
    $stmt->close();
    
    // 获取最新点赞数
    $stmt2 = $conn->prepare("SELECT COUNT(*) as total FROM news_interactions WHERE news_id = ? AND liked = 1");
    $stmt2->bind_param("s", $newsId);
    $stmt2->execute();
    $totalLikes = $stmt2->get_result()->fetch_assoc()['total'];
    $stmt2->close();
    
    successResponse($newLiked ? '已点赞' : '已取消点赞', [
        'liked' => (bool)$newLiked,
        'likes' => (int)$totalLikes
    ]);
}

function handleComment() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    $newsId = $input['news_id'] ?? '';
    $text = trim($input['text'] ?? '');
    
    if (empty($newsId)) errorResponse('缺少 news_id');
    if (empty($text)) errorResponse('请输入评论内容');
    if (strlen($text) > 500) errorResponse('评论内容不能超过500个字符');
    
    $conn = getDB();
    $stmt = $conn->prepare("INSERT INTO news_comments (news_id, user_id, comment_text) VALUES (?, ?, ?)");
    $stmt->bind_param("sis", $newsId, $user['id'], $text);
    $stmt->execute();
    $commentId = $conn->insert_id;
    $stmt->close();
    
    successResponse('评论发表成功', [
        'id' => (int)$commentId,
        'author' => $user['username'],
        'text' => $text,
        'time' => date('Y-m-d H:i:s')
    ]);
}

function handleDeleteComment() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);
    $commentId = $input['comment_id'] ?? 0;
    
    if (!$commentId) errorResponse('缺少 comment_id');
    
    $conn = getDB();
    // 只能删除自己的评论
    $stmt = $conn->prepare("DELETE FROM news_comments WHERE id = ? AND user_id = ?");
    $stmt->bind_param("ii", $commentId, $user['id']);
    $stmt->execute();
    
    if ($stmt->affected_rows > 0) {
        successResponse('删除成功');
    } else {
        $stmt->close();
        errorResponse('评论不存在或无权删除');
    }
    $stmt->close();
}
?>