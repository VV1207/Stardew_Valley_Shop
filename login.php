<?php
require_once 'db_config.php';
initDatabase();

$error_msg = '';
$show_error = false;
$field_errors = [];
$not_found_username = '';
$show_not_found = false;

// 处理登录表单提交
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = isset($_POST['username']) ? trim($_POST['username']) : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';
    $captcha_input = isset($_POST['captcha']) ? trim($_POST['captcha']) : '';

    // 格式验证
    $valid = true;

    if (empty($username)) {
        $field_errors['username'] = '请输入用户名';
        $valid = false;
    } elseif (strlen($username) < 2 || strlen($username) > 20) {
        $field_errors['username'] = '用户名长度应为2-20个字符';
        $valid = false;
    } elseif (!preg_match('/^[\x{4e00}-\x{9fa5}a-zA-Z0-9_]+$/u', $username)) {
        $field_errors['username'] = '用户名只能包含中文、字母、数字和下划线';
        $valid = false;
    }

    if (empty($password)) {
        $field_errors['password'] = '请输入密码';
        $valid = false;
    } elseif (strlen($password) < 6) {
        $field_errors['password'] = '密码长度不能少于6位';
        $valid = false;
    }

    // 验证码验证
    if (empty($captcha_input)) {
        $field_errors['captcha'] = '请输入验证码';
        $valid = false;
    } elseif (!isset($_SESSION['captcha']) || strtolower($captcha_input) !== $_SESSION['captcha']) {
        $field_errors['captcha'] = '验证码错误，请重新输入';
        $valid = false;
    }

    if ($valid) {
        $conn = getDBConnection();
        
        // 查询数据库中是否存在该用户
        $stmt = $conn->prepare("SELECT id, username, password, address, email, last_login FROM users WHERE username = ?");
        $stmt->bind_param("s", $username);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows === 0) {
            // 账户不存在，提示并跳转到注册页面
            $conn->close();
            unset($_SESSION['captcha']);
            echo "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>
            <script>
                alert('该用户尚未注册，请先注册！');
                window.location.href = 'register.php?from=login&username=" . urlencode($username) . "';
            </script>
            </body></html>";
            exit;
        }

        // 账户存在，验证密码
        $user = $result->fetch_assoc();
        if (!password_verify($password, $user['password'])) {
            $error_msg = '密码错误，请重新输入';
            $show_error = true;
            unset($_SESSION['captcha']);
        } else {
            // 登录成功，更新最后登录时间
            $now = date('Y-m-d H:i:s');
            $update_stmt = $conn->prepare("UPDATE users SET last_login = ? WHERE id = ?");
            $update_stmt->bind_param("si", $now, $user['id']);
            $update_stmt->execute();
            $update_stmt->close();

            // 保存用户信息到 session
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            $_SESSION['login_time'] = $now;

            // 保存到 localStorage
            $user_data = json_encode([
                'username' => $user['username'],
                'email' => $user['email'] ?: '',
                'address' => $user['address'] ?: '鹈鹕镇事务大厅',
                'loginTime' => $now
            ]);

            $conn->close();
            unset($_SESSION['captcha']);

            // 支持 from 参数，跳转回来源页面
            $from = isset($_GET['from']) && $_GET['from'] !== '' ? $_GET['from'] : 'index.html';
            // 防止 XSS：只允许本地跳转
            if (strpos($from, 'http') !== false) $from = 'index.html';

            echo "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>
            <script>
                localStorage.setItem('stardew_user', '" . addslashes($user_data) . "');
                window.location.href = '" . addslashes($from) . "';
            </script>
            </body></html>";
            exit;
        }
        $stmt->close();
        $conn->close();
    }
}

// 生成验证码 session
if (!isset($_SESSION['captcha'])) {
    $chars = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz';
    $captcha_code = '';
    for ($i = 0; $i < 4; $i++) {
        $captcha_code .= $chars[random_int(0, strlen($chars) - 1)];
    }
    $_SESSION['captcha'] = strtolower($captcha_code);
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>星露谷 · 用户登录</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px; }
        footer { margin-top: 30px; }
        .password-group { position: relative; }
        .password-group input { padding-right: 45px; }
        .toggle-pwd {
            position: absolute;
            right: 14px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            font-size: 1.1rem;
            opacity: 0.5;
            transition: opacity 0.2s;
        }
        .toggle-pwd:hover { opacity: 0.9; }
        .server-error {
            background: #fde6e6;
            color: #b5573a;
            padding: 10px 16px;
            border-radius: 12px;
            font-size: 0.82rem;
            margin-bottom: 14px;
            text-align: center;
            border: 1px solid #f5c6c6;
        }
        .register-hint {
            text-align: center;
            margin-top: 12px;
            font-size: 0.82rem;
            color: #6b5e4a;
        }
        .register-hint a {
            color: #578b34;
            font-weight: 600;
            text-decoration: none;
        }
        .register-hint a:hover { text-decoration: underline; }
        .captcha-row {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .captcha-row input {
            flex: 1;
        }
        .captcha-row img {
            height: 42px;
            border-radius: 12px;
            cursor: pointer;
            border: 2px solid #dcd0bc;
            transition: border-color 0.2s;
        }
        .captcha-row img:hover {
            border-color: #88aa66;
        }
        .captcha-hint {
            font-size: 0.72rem;
            color: #9a8a7a;
            margin-top: 4px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="avatar">🌾</div>
            <h1>欢迎回到星露谷</h1>
            <p>请输入用户名、密码和验证码登录</p>
        </div>

        <?php if ($show_error): ?>
        <div class="server-error"><?php echo htmlspecialchars($error_msg); ?></div>
        <?php endif; ?>

        <form id="loginForm" method="POST" action="login.php<?php echo isset($_GET['from']) && $_GET['from'] !== '' ? '?from=' . urlencode($_GET['from']) : ''; ?>" novalidate>
            <div class="form-group" id="nameGroup">
                <label>👤 用户名 <span class="required">*</span></label>
                <input type="text" id="username" name="username" placeholder="请输入用户名" maxlength="20" autocomplete="off"
                    value="<?php echo isset($_POST['username']) ? htmlspecialchars($_POST['username']) : ''; ?>">
                <div class="error-msg" id="usernameError">请输入用户名</div>
            </div>

            <div class="form-group" id="passwordGroup">
                <label>🔒 密码 <span class="required">*</span></label>
                <div class="password-group">
                    <input type="password" id="password" name="password" placeholder="请输入密码（至少6位）" maxlength="50" autocomplete="off">
                    <button type="button" class="toggle-pwd" onclick="togglePassword()">👁</button>
                </div>
                <div class="error-msg" id="passwordError">请输入密码</div>
            </div>

            <div class="form-group" id="captchaGroup">
                <label>🔤 验证码 <span class="required">*</span></label>
                <div class="captcha-row">
                    <input type="text" id="captcha" name="captcha" placeholder="请输入验证码" maxlength="4" autocomplete="off" style="text-transform:uppercase;">
                    <img src="captcha.php" alt="验证码" id="captchaImg" title="点击刷新验证码" onclick="refreshCaptcha()">
                </div>
                <div class="captcha-hint">💡 点击图片可刷新验证码</div>
                <div class="error-msg" id="captchaError">请输入验证码</div>
            </div>

            <button type="submit" class="submit-btn">🌻 确认登录</button>
        </form>

        <div class="register-hint">
            还没有账户？<a href="register.php">立即注册</a>
        </div>

        <div class="back-link">
            <a href="index.html">← 返回商店首页</a>
        </div>
    </div>

    <footer>
        ⭐ 数据来源: 星露谷中文维基百科 · 图片版权归 ConcernedApe 所有 ⭐<br>
        网页制作：陈薇羽 · 联系方式：1152629204@qq.com
    </footer>

    <script>
        // 显示/隐藏密码
        function togglePassword() {
            var pwdInput = document.getElementById('password');
            var btn = document.querySelector('.toggle-pwd');
            if (pwdInput.type === 'password') {
                pwdInput.type = 'text';
                btn.textContent = '🙈';
            } else {
                pwdInput.type = 'password';
                btn.textContent = '👁';
            }
        }

        // 刷新验证码
        function refreshCaptcha() {
            var img = document.getElementById('captchaImg');
            img.src = 'captcha.php?' + new Date().getTime();
        }

        var form = document.getElementById('loginForm');
        var usernameInput = document.getElementById('username');
        var passwordInput = document.getElementById('password');
        var captchaInput = document.getElementById('captcha');

        // 实时清除错误状态
        usernameInput.addEventListener('input', function() {
            document.getElementById('nameGroup').classList.remove('error');
            document.getElementById('usernameError').textContent = '请输入用户名';
        });
        passwordInput.addEventListener('input', function() {
            document.getElementById('passwordGroup').classList.remove('error');
        });
        captchaInput.addEventListener('input', function() {
            document.getElementById('captchaGroup').classList.remove('error');
        });

        form.addEventListener('submit', function(e) {
            var valid = true;

            // 验证用户名
            var username = usernameInput.value.trim();
            if (!username) {
                document.getElementById('nameGroup').classList.add('error');
                document.getElementById('usernameError').textContent = '请输入用户名';
                valid = false;
            } else if (username.length < 2 || username.length > 20) {
                document.getElementById('nameGroup').classList.add('error');
                document.getElementById('usernameError').textContent = '用户名长度应为2-20个字符';
                valid = false;
            } else if (!/^[\u4e00-\u9fa5a-zA-Z0-9_]+$/.test(username)) {
                document.getElementById('nameGroup').classList.add('error');
                document.getElementById('usernameError').textContent = '用户名只能包含中文、字母、数字和下划线';
                valid = false;
            }

            // 验证密码
            var password = passwordInput.value;
            if (!password) {
                document.getElementById('passwordGroup').classList.add('error');
                document.getElementById('passwordError').textContent = '请输入密码';
                valid = false;
            } else if (password.length < 6) {
                document.getElementById('passwordGroup').classList.add('error');
                document.getElementById('passwordError').textContent = '密码长度不能少于6位';
                valid = false;
            }

            // 验证验证码
            var captcha = captchaInput.value.trim();
            if (!captcha) {
                document.getElementById('captchaGroup').classList.add('error');
                document.getElementById('captchaError').textContent = '请输入验证码';
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
                refreshCaptcha();
            }
        });
    </script>
</body>
</html>