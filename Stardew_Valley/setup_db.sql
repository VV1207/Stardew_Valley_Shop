-- 星露谷商店数据库建表脚本
-- 使用方法：在 phpMyAdmin 或 MySQL 命令行中执行此脚本

CREATE DATABASE IF NOT EXISTS `stardew_valley` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `stardew_valley`;

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(255) NOT NULL COMMENT '密码（bcrypt加密）',
    `address` VARCHAR(100) DEFAULT '鹈鹕镇事务中心' COMMENT '住址',
    `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `last_login` DATETIME DEFAULT NULL COMMENT '最后登录时间',
    INDEX `idx_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';