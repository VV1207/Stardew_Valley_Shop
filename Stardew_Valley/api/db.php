<?php
/**
 * 数据库连接和辅助函数
 */
session_start();

define('DB_HOST', 'localhost');
define('DB_PORT', 3316);
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'stardew_valley');

/**
 * 获取数据库连接
 */
function getDB() {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
    if ($conn->connect_error) {
        http_response_code(500);
        die(json_encode(['error' => '数据库连接失败: ' . $conn->connect_error]));
    }
    $conn->set_charset("utf8mb4");
    return $conn;
}

/**
 * 获取当前登录用户
 * @return array|null 用户信息或null
 */
function getCurrentUser() {
    if (!isset($_SESSION['user_id'])) {
        return null;
    }
    $conn = getDB();
    $stmt = $conn->prepare("SELECT id, username, email, address, created_at, last_login FROM users WHERE id = ?");
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    $stmt->close();
    return $user;
}

/**
 * 需要登录才能访问的API
 */
function requireLogin() {
    $user = getCurrentUser();
    if (!$user) {
        http_response_code(401);
        die(json_encode(['error' => '请先登录']));
    }
    return $user;
}

/**
 * JSON响应
 */
function jsonResponse($data, $code = 200) {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * 成功响应
 */
function successResponse($message = '操作成功', $data = null) {
    $response = ['success' => true, 'message' => $message];
    if ($data !== null) {
        $response['data'] = $data;
    }
    jsonResponse($response);
}

/**
 * 错误响应
 */
function errorResponse($message = '操作失败', $code = 400) {
    jsonResponse(['success' => false, 'error' => $message], $code);
}
?>