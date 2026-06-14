<?php
require_once 'db_config.php';
initDatabase();

$error_msg = '';
$show_error = false;
$field_errors = [];
$old_username = '';
$old_email = '';

// 从登录页跳转过来，预填用户名
if (isset($_GET['from']) && $_GET['from'] === 'login' && isset($_GET['username'])) {
    $old_username = htmlspecialchars($_GET['username']);
}

// 处理注册表单提交
if (isset($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = isset($_POST['username']) ? trim($_POST['username']) : '';
    $email = isset($_POST['email']) ? trim($_POST['email']) : '';
    $password = isset($_POST['password']) ? $_POST['password'] : '';
    $confirm_password = isset($_POST['confirm_password']) ? $_POST['confirm_password'] : '';

    $old_username = htmlspecialchars($username);
    $old_email = htmlspecialchars($email);

    // 格式验证
    $valid = true;

    // 用户名验证
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

    // 邮箱验证
    if (empty($email)) {
        $field_errors['email'] = '请输入联系邮箱';
        $valid = false;
    } elseif (!preg_match('/^[^\s@]+@[^\s@]+\.[^\s@]+$/', $email)) {
        $field_errors['email'] = '请输入正确的邮箱地址';
        $valid = false;
    }

    // 密码验证
    if (empty($password)) {
        $field_errors['password'] = '请输入密码';
        $valid = false;
    } elseif (strlen($password) < 6) {
        $field_errors['password'] = '密码长度不能少于6位';
        $valid = false;
    } elseif (strlen($password) > 50) {
        $field_errors['password'] = '密码长度不能超过50个字符';
        $valid = false;
    }

    // 确认密码验证
    if (empty($confirm_password)) {
        $field_errors['confirm_password'] = '请再次输入密码';
        $valid = false;
    } elseif ($password !== $confirm_password) {
        $field_errors['confirm_password'] = '两次输入的密码不一致';
        $valid = false;
    }

    if ($valid) {
        $conn = getDBConnection();

        // 检查用户名是否已存在
        $check_stmt = $conn->prepare("SELECT id FROM users WHERE username = ?");
        $check_stmt->bind_param("s", $username);
        $check_stmt->execute();
        $check_result = $check_stmt->get_result();

        if ($check_result->num_rows > 0) {
            $error_msg = '该用户名已被注册，请选择其他用户名';
            $show_error = true;
        } else {
            // 创建新用户（住址默认"鹈鹕镇事务大厅"，由用户在 delivery.html 中修改）
            $hashed_password = password_hash($password, PASSWORD_DEFAULT);
            $now = date('Y-m-d H:i:s');

            $insert_stmt = $conn->prepare("INSERT INTO users (username, password, email, address, created_at, last_login) VALUES (?, ?, ?, '鹈鹕镇事务大厅', ?, ?)");
            $insert_stmt->bind_param("ssss", $username, $hashed_password, $email, $now, $now);
            
            if ($insert_stmt->execute()) {
                // 自动登录
                $new_user_id = $conn->insert_id;
                $_SESSION['user_id'] = $new_user_id;
                $_SESSION['username'] = $username;
                $_SESSION['login_time'] = $now;

                $user_data = json_encode([
                    'username' => $username,
                    'email' => $email,
                    'address' => '鹈鹕镇事务大厅',
                    'loginTime' => $now
                ]);

                echo "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>
                <script>
                    localStorage.setItem('stardew_user', '" . addslashes($user_data) . "');
                    alert('注册成功！欢迎来到星露谷！');
                    window.location.href = 'index.html';
                </script>
                </body></html>";
                $insert_stmt->close();
                $conn->close();
                exit;
            } else {
                $error_msg = '注册失败，请稍后重试';
                $show_error = true;
            }
            $insert_stmt->close();
        }
        $check_stmt->close();
        $conn->close();
    }
}
?>
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>星露谷 · 用户注册</title>
    <link rel="stylesheet" href="style.css">
    <style>
        body { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 16px; }
        .login-container { max-width: 460px; }
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
        .login-hint {
            text-align: center;
            margin-top: 12px;
            font-size: 0.82rem;
            color: #6b5e4a;
        }
        .login-hint a {
            color: #578b34;
            font-weight: 600;
            text-decoration: none;
        }
        .login-hint a:hover { text-decoration: underline; }
        .password-strength {
            display: flex;
            gap: 4px;
            margin-top: 6px;
        }
        .strength-bar {
            flex: 1;
            height: 4px;
            background: #e0d4b8;
            border-radius: 4px;
            transition: background 0.3s;
        }
        .strength-bar.weak { background: #b5573a; }
        .strength-bar.medium { background: #c57f1e; }
        .strength-bar.strong { background: #578b34; }
        .strength-text {
            font-size: 0.72rem;
            margin-top: 2px;
            color: #9a8a7a;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 0.7rem;
            color: #b9ab92;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="avatar">🌱</div>
            <h1>注册新账户</h1>
            <p>加入星露谷，开启你的农场之旅</p>
        </div>

        <?php if ($show_error): ?>
        <div class="server-error"><?php echo htmlspecialchars($error_msg); ?></div>
        <?php endif; ?>

        <form id="registerForm" method="POST" action="register.php" novalidate>
            <div class="form-group" id="nameGroup">
                <label>👤 用户名 <span class="required">*</span></label>
                <input type="text" id="username" name="username" placeholder="2-20个字符，中文/字母/数字/下划线" maxlength="20" autocomplete="off"
                    value="<?php echo $old_username; ?>">
                <div class="error-msg" id="usernameError">请输入用户名</div>
            </div>

            <div class="form-group" id="emailGroup">
                <label>📧 联系邮箱 <span class="required">*</span></label>
                <input type="email" id="email" name="email" placeholder="example@email.com" maxlength="100" autocomplete="off"
                    value="<?php echo $old_email; ?>">
                <div class="error-msg" id="emailError">请输入正确的邮箱地址</div>
            </div>

            <div class="form-group" id="passwordGroup">
                <label>🔒 密码 <span class="required">*</span></label>
                <div class="password-group">
                    <input type="password" id="password" name="password" placeholder="请输入密码（至少6位）" maxlength="50" autocomplete="off">
                    <button type="button" class="toggle-pwd" onclick="togglePassword('password', this)">👁</button>
                </div>
                <div class="password-strength">
                    <div class="strength-bar" id="str1"></div>
                    <div class="strength-bar" id="str2"></div>
                    <div class="strength-bar" id="str3"></div>
                </div>
                <div class="strength-text" id="strengthText"></div>
                <div class="error-msg" id="passwordError">请输入密码</div>
            </div>

            <div class="form-group" id="confirmGroup">
                <label>🔒 确认密码 <span class="required">*</span></label>
                <div class="password-group">
                    <input type="password" id="confirm_password" name="confirm_password" placeholder="请再次输入密码" maxlength="50" autocomplete="off">
                    <button type="button" class="toggle-pwd" onclick="togglePassword('confirm_password', this)">👁</button>
                </div>
                <div class="error-msg" id="confirmError">请再次输入密码</div>
            </div>

            <button type="submit" class="submit-btn">🌻 确认注册</button>
        </form>

        <div class="login-hint">
            已有账户？<a href="login.php">立即登录</a>
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
        // 如果已登录，跳转回首页
        const existingUser = localStorage.getItem('stardew_user');
        if (existingUser) {
            window.location.href = 'index.html';
        }

        // 显示/隐藏密码
        function togglePassword(fieldId, btn) {
            var input = document.getElementById(fieldId);
            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = '🙈';
            } else {
                input.type = 'password';
                btn.textContent = '👁';
            }
        }

        // 密码强度检测
        function checkPasswordStrength(pwd) {
            var score = 0;
            if (pwd.length >= 6) score++;
            if (pwd.length >= 10) score++;
            if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) score++;
            if (/\d/.test(pwd)) score++;
            if (/[^a-zA-Z0-9]/.test(pwd)) score++;

            var bars = [document.getElementById('str1'), document.getElementById('str2'), document.getElementById('str3')];
            var text = document.getElementById('strengthText');
            
            bars.forEach(function(b) { b.className = 'strength-bar'; });
            text.textContent = '';

            if (pwd.length === 0) return;
            
            if (score <= 1) {
                bars[0].classList.add('weak');
                text.textContent = '密码强度：弱';
                text.style.color = '#b5573a';
            } else if (score <= 3) {
                bars[0].classList.add('medium');
                bars[1].classList.add('medium');
                text.textContent = '密码强度：中';
                text.style.color = '#c57f1e';
            } else {
                bars.forEach(function(b) { b.classList.add('strong'); });
                text.textContent = '密码强度：强';
                text.style.color = '#578b34';
            }
        }

        function isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        }

        document.getElementById('password').addEventListener('input', function() {
            checkPasswordStrength(this.value);
            document.getElementById('passwordGroup').classList.remove('error');
        });

        // 实时清除错误状态
        document.getElementById('username').addEventListener('input', function() {
            document.getElementById('nameGroup').classList.remove('error');
        });
        document.getElementById('email').addEventListener('input', function() {
            if (isValidEmail(this.value.trim())) {
                document.getElementById('emailGroup').classList.remove('error');
            }
        });
        document.getElementById('confirm_password').addEventListener('input', function() {
            document.getElementById('confirmGroup').classList.remove('error');
        });

        // 表单验证
        document.getElementById('registerForm').addEventListener('submit', function(e) {
            var valid = true;

            var username = document.getElementById('username').value.trim();
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

            var email = document.getElementById('email').value.trim();
            if (!email) {
                document.getElementById('emailGroup').classList.add('error');
                document.getElementById('emailError').textContent = '请输入联系邮箱';
                valid = false;
            } else if (!isValidEmail(email)) {
                document.getElementById('emailGroup').classList.add('error');
                document.getElementById('emailError').textContent = '请输入正确的邮箱地址';
                valid = false;
            }

            var password = document.getElementById('password').value;
            if (!password) {
                document.getElementById('passwordGroup').classList.add('error');
                document.getElementById('passwordError').textContent = '请输入密码';
                valid = false;
            } else if (password.length < 6) {
                document.getElementById('passwordGroup').classList.add('error');
                document.getElementById('passwordError').textContent = '密码长度不能少于6位';
                valid = false;
            }

            var confirmPassword = document.getElementById('confirm_password').value;
            if (!confirmPassword) {
                document.getElementById('confirmGroup').classList.add('error');
                document.getElementById('confirmError').textContent = '请再次输入密码';
                valid = false;
            } else if (password !== confirmPassword) {
                document.getElementById('confirmGroup').classList.add('error');
                document.getElementById('confirmError').textContent = '两次输入的密码不一致';
                valid = false;
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    </script>
</body>
</html>