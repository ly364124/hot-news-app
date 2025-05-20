-- 创建数据库
CREATE DATABASE IF NOT EXISTS hot_news CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE hot_news;

-- 创建用户并授权（如果需要）
CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON hot_news.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

-- 创建热门话题表
CREATE TABLE IF NOT EXISTS hot_topics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(512) NOT NULL,
    source ENUM('zhihu', 'weibo') NOT NULL,
    `rank` INT NOT NULL,
    hot_value VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_rank (`rank`),
    INDEX idx_source (source),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入测试数据
INSERT INTO hot_topics (title, url, source, `rank`, hot_value) VALUES
('测试知乎话题1', 'https://www.zhihu.com/question/123', 'zhihu', 1, '1000'),
('测试知乎话题2', 'https://www.zhihu.com/question/456', 'zhihu', 2, '800'),
('测试微博话题1', 'https://weibo.com/123', 'weibo', 1, '5000'),
('测试微博话题2', 'https://weibo.com/456', 'weibo', 2, '3000'); 