<?php
// 数据库配置
define('DB_HOST', 'localhost');
define('DB_PORT', 3316);
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'stardew_valley');

// 创建数据库连接
function getDBConnection() {
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
    if ($conn->connect_error) {
        die("数据库连接失败: " . $conn->connect_error);
    }
    $conn->set_charset("utf8mb4");
    return $conn;
}

// 初始化数据库表（如果不存在）
function initDatabase() {
    // 先连接到 MySQL 服务器（不指定数据库）
    $conn = new mysqli(DB_HOST, DB_USER, DB_PASS, '', DB_PORT);
    if ($conn->connect_error) {
        die("数据库服务器连接失败: " . $conn->connect_error);
    }
    $conn->set_charset("utf8mb4");

    // 创建数据库（如果不存在）
    $conn->query("CREATE DATABASE IF NOT EXISTS `stardew_valley` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
    $conn->select_db("stardew_valley");

    // 创建用户表
    $sql = "CREATE TABLE IF NOT EXISTS `users` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `username` VARCHAR(50) NOT NULL UNIQUE,
        `password` VARCHAR(255) NOT NULL,
        `address` VARCHAR(100) DEFAULT '鹈鹕镇事务中心',
        `email` VARCHAR(100) DEFAULT NULL,
        `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
        `last_login` DATETIME DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci";
    
    $conn->query($sql);
    $conn->close();
}

// 启动会话
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>