<?php
/**
 * 用户认证 API
 * 
 * POST /api/auth.php?action=login    - 登录
 * POST /api/auth.php?action=register - 注册
 * GET  /api/auth.php?action=me       - 获取当前用户
 * POST /api/auth.php?action=logout   - 退出登录
 * PUT  /api/auth.php?action=profile  - 更新个人资料
 */
require_once __DIR__ . '/db.php';

header('Content-Type: application/json; charset=utf-8');

$action = isset($_GET['action']) ? $_GET['action'] : '';

switch ($action) {
    case 'login':
        handleLogin();
        break;
    case 'register':
        handleRegister();
        break;
    case 'me':
        handleMe();
        break;
    case 'logout':
        handleLogout();
        break;
    case 'profile':
        handleProfile();
        break;
    default:
        errorResponse('未知操作: ' . $action, 404);
}

function handleLogin() {
    $input = json_decode(file_get_contents('php://input'), true);
    $username = trim($input['username'] ?? '');
    $password = $input['password'] ?? '';

    if (empty($username)) {
        errorResponse('请输入用户名');
    }
    if (empty($password)) {
        errorResponse('请输入密码');
    }

    $conn = getDB();
    $stmt = $conn->prepare("SELECT id, username, password, email, address, created_at, last_login FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();
    $stmt->close();

    if (!$user) {
        errorResponse('该用户尚未注册');
    }

    if (!password_verify($password, $user['password'])) {
        errorResponse('密码错误');
    }

    // 设置 Session
    $_SESSION['user_id'] = $user['id'];
    $_SESSION['username'] = $user['username'];

    // 更新最后登录时间
    $now = date('Y-m-d H:i:s');
    $stmt2 = $conn->prepare("UPDATE users SET last_login = ? WHERE id = ?");
    $stmt2->bind_param("si", $now, $user['id']);
    $stmt2->execute();
    $stmt2->close();

    unset($user['password']); // 不返回密码
    $user['loginTime'] = $now;

    successResponse('登录成功', ['user' => $user]);
}

function handleRegister() {
    $input = json_decode(file_get_contents('php://input'), true);
    $username = trim($input['username'] ?? '');
    $email = trim($input['email'] ?? '');
    $password = $input['password'] ?? '';
    $confirm = $input['confirm_password'] ?? '';

    // 验证
    if (empty($username)) errorResponse('请输入用户名');
    if (strlen($username) < 2 || strlen($username) > 20) errorResponse('用户名长度应为2-20个字符');
    if (!preg_match('/^[\x{4e00}-\x{9fa5}a-zA-Z0-9_]+$/u', $username)) {
        errorResponse('用户名只能包含中文、字母、数字和下划线');
    }
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        errorResponse('请输入正确的邮箱地址');
    }
    if (strlen($password) < 6) errorResponse('密码长度不能少于6位');
    if ($password !== $confirm) errorResponse('两次输入的密码不一致');

    $conn = getDB();

    // 检查用户名是否已存在
    $stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    if ($stmt->get_result()->num_rows > 0) {
        $stmt->close();
        errorResponse('该用户名已被注册');
    }
    $stmt->close();

    // 创建用户
    $hashed = password_hash($password, PASSWORD_DEFAULT);
    $now = date('Y-m-d H:i:s');
    $stmt = $conn->prepare("INSERT INTO users (username, password, email, address, created_at, last_login) VALUES (?, ?, ?, '鹈鹕镇事务大厅', ?, ?)");
    $stmt->bind_param("ssss", $username, $hashed, $email, $now, $now);
    $stmt->execute();
    $userId = $conn->insert_id;
    $stmt->close();

    // 自动登录
    $_SESSION['user_id'] = $userId;
    $_SESSION['username'] = $username;

    $user = [
        'id' => $userId,
        'username' => $username,
        'email' => $email,
        'address' => '鹈鹕镇事务大厅',
        'created_at' => $now,
        'last_login' => $now
    ];

    successResponse('注册成功', ['user' => $user]);
}

function handleMe() {
    $user = getCurrentUser();
    if (!$user) {
        jsonResponse(['success' => false, 'error' => '未登录', 'loggedIn' => false]);
        return;
    }
    successResponse('已登录', ['user' => $user, 'loggedIn' => true]);
}

function handleLogout() {
    session_destroy();
    successResponse('已退出登录');
}

function handleProfile() {
    $user = requireLogin();
    $input = json_decode(file_get_contents('php://input'), true);

    $conn = getDB();
    $fields = [];
    $types = '';
    $values = [];

    if (isset($input['address'])) {
        $fields[] = 'address = ?';
        $types .= 's';
        $values[] = $input['address'];
    }
    if (isset($input['email'])) {
        $fields[] = 'email = ?';
        $types .= 's';
        $values[] = $input['email'];
    }

    if (empty($fields)) {
        errorResponse('没有要更新的内容');
    }

    $values[] = $user['id'];
    $types .= 'i';
    $sql = "UPDATE users SET " . implode(', ', $fields) . " WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param($types, ...$values);
    $stmt->execute();
    $stmt->close();

    $updatedUser = getCurrentUser();
    successResponse('更新成功', ['user' => $updatedUser]);
}
?>