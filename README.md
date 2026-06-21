# 🌾 星露谷 · 全物品图谱商店

一个以《星露谷物语》(Stardew Valley) 为主题的在线购物商店网站，展示星露谷全部物品图谱，支持搜索筛选、购物车、用户系统和订单管理。

## ✨ 功能特性

- **商品浏览**：561 种星露谷物品，涵盖作物、动物、果树、工匠制品、矿物、渔具、武器等 20+ 分类
- **搜索与筛选**：支持按名称搜索、按分类筛选，分页显示（每页 16 件）
- **购物车系统**：添加商品、调整数量、品质选择、实时价格计算
- **结账订单**：订单明细预览、一键结账、村民配送/自提
- **用户系统**：注册、登录（含验证码）、个人资料管理
- **收藏功能**：收藏/取消收藏喜爱的物品
- **村民赠送反应**：查看每个物品的村民喜好（最爱/喜欢/一般/不喜欢/讨厌）
- **左侧推荐栏**：精品推荐（价格前10随机5）、村民最爱、限时热卖
- **背景音乐**：内置星露谷原声音乐播放器，跨页面连续播放
- **新闻页面**：星露谷动态与活动公告
- **响应式设计**：适配桌面和移动端

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | HTML5 + CSS3 + 原生 JavaScript |
| 后端 | PHP（API 接口） |
| 数据库 | MySQL（utf8mb4） |
| 服务器 | XAMPP（Apache + MySQL） |
| 版本控制 | Git + GitHub |

## 📁 项目结构

```
Stardew_Valley/
├── index.html          # 商店首页（商品浏览、购物车、搜索筛选）
├── news.html           # 新闻页面（星闻露谷）
├── delivery.html       # 配送服务页面
├── profile.html        # 用户个人资料页面
├── login.php           # 用户登录（含验证码）
├── register.php        # 用户注册
├── style.css           # 全局样式（星露谷主题）
├── items_data.js       # 物品数据（561 条）
├── music-player.js     # 共享音乐播放器脚本
├── db_config.php       # 数据库配置
├── setup_db.sql        # 数据库建表脚本
├── captcha.php         # 验证码生成
├── api/                # 后端 API 接口
│   ├── auth.php        # 用户认证（登录/注册/登出）
│   ├── cart.php        # 购物车管理
│   ├── favorites.php   # 收藏功能
│   ├── orders.php      # 订单管理
│   ├── reviews.php     # 商品评价
│   ├── feedback.php    # 用户反馈
│   ├── interact.php    # 互动功能
│   └── db.php          # 数据库连接
├── audio/              # 背景音乐文件
├── images/             # 物品图片、村民头像、背景图
└── fonts/              # 自定义字体
```

## 🚀 快速开始

### 环境要求

- XAMPP（Apache + MySQL + PHP）
- PHP 7.4+
- MySQL 5.7+

### 安装步骤

1. 克隆项目到 XAMPP 的 `htdocs` 目录：
   ```bash
   git clone https://github.com/VV1207/Stardew_Valley_Shop.git
   cd Stardew_Valley_Shop
   ```

2. 启动 XAMPP 的 Apache 和 MySQL 服务

3. 执行数据库建表脚本：
   - 打开 phpMyAdmin（http://localhost/phpmyadmin）
   - 创建数据库
   - 导入 `setup_db.sql` 文件

4. 修改数据库配置：
   - 编辑 `db_config.php`（如需要，修改数据库连接信息）

5. 在浏览器中打开：
   ```
   http://localhost/Stardew_Valley_Shop/
   ```

## 📸 页面预览

- 🏠 **商店首页**：商品网格展示 + 左侧推荐栏 + 右侧购物车
- 📰 **星闻露谷**：新闻列表 + 分类筛选
- 📦 **配送服务**：订单追踪 + 配送状态
- 👤 **个人中心**：用户信息 + 收藏列表 + 订单历史
- 🔑 **登录/注册**：星露谷风格的表单界面

## 👩‍💻 作者

**陈薇羽** — 1152629204@qq.com

## 📝 数据来源

- 星露谷中文维基百科
- 图片版权归 ConcernedApe 所有

## 📄 License

本项目仅供学习交流使用。