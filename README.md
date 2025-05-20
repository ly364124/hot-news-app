# 实时热搜资讯平台

这是一个实时抓取知乎和微博热搜话题的资讯平台，包含后端 API 服务和前端展示界面。

## 功能特点

- 🔥 实时聚合：同时展示知乎和微博的热搜话题，让您不错过任何热点
- 🎯 智能分类：支持按平台（知乎/微博）筛选，快速找到感兴趣的内容
- 📊 热度追踪：实时显示话题排名和热度值，了解话题热度变化
- ⚡ 自动更新：定时自动抓取最新热搜数据，保持信息实时性
- 💾 数据持久：自动保存历史热搜数据，支持数据分析和趋势追踪
- 🎨 优雅界面：采用现代化 UI 设计，支持响应式布局，提供流畅的浏览体验
- 🔍 快速跳转：点击话题可直接跳转到对应平台查看详情
- 📱 移动适配：完美支持移动端访问，随时随地查看热搜

## 技术栈

### 后端
- FastAPI：高性能的 Python Web 框架
- SQLAlchemy：强大的 ORM 框架
- APScheduler：任务调度系统
- aiohttp：异步 HTTP 客户端
- BeautifulSoup4：HTML 解析库
- MySQL：数据存储

### 前端
- Vue 3：渐进式 JavaScript 框架
- TypeScript：类型安全的 JavaScript 超集
- Element Plus：基于 Vue 3 的组件库
- Pinia：Vue 的状态管理库
- Vite：下一代前端构建工具

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+


## 项目结构

```
hot-news-app/
├── app/                    # 后端应用
│   ├── api/               # API 路由
│   ├── core/              # 核心配置
│   ├── crawlers/          # 爬虫模块
│   ├── models/            # 数据模型
│   └── schemas/           # 数据验证
└── frontend/              # 前端应用
    ├── src/
    │   ├── api/          # API 调用
    │   ├── components/   # 组件
    │   ├── router/       # 路由
    │   ├── stores/       # 状态管理
    │   └── views/        # 页面
    └── public/           # 静态资源
```

## 安装和运行

### 后端服务

1. 创建并激活 Python 虚拟环境：
```bash
python -m venv venv
```

在 Windows 系统中激活虚拟环境：
```bash
# 如果使用 PowerShell，需要先设置执行策略（以管理员身份运行 PowerShell）：
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后激活虚拟环境：
.\venv\Scripts\activate

# 或者使用 CMD：
venv\Scripts\activate.bat
```

在 Linux/Mac 系统中激活虚拟环境：
```bash
source venv/bin/activate
```

2. 安装依赖：
```bash
# 使用国内镜像源安装依赖（推荐）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 如果遇到超时问题，可以尝试其他镜像源：
# 阿里云：https://mirrors.aliyun.com/pypi/simple/
# 豆瓣：https://pypi.douban.com/simple/
# 华为云：https://repo.huaweicloud.com/repository/pypi/simple/
```

3. 配置数据库：
   - 创建 MySQL 数据库：
   ```sql
   CREATE DATABASE hot_news CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   - 创建并配置环境变量文件：
     ```bash
     # 复制环境变量示例文件
     cp .env.example .env
     ```
   - 编辑 `.env` 文件，修改以下配置：
     ```
     # 数据库配置（必填）
     DATABASE_URL=mysql+pymysql://root:password@localhost/hot_news
     # 将 root 和 password 替换为您的 MySQL 用户名和密码

     # 知乎配置（必填）
     ZHIHU_COOKIE=
     # 从浏览器中获取知乎的 Cookie

     # 爬虫配置（可选）
     CRAWL_INTERVAL=30  # 爬虫更新间隔（分钟）
     USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36

     # 代理配置（可选）
     # HTTP_PROXY=http://127.0.0.1:7890
     # HTTPS_PROXY=http://127.0.0.1:7890
     ```

4. 运行后端服务：
```bash
uvicorn app.main:app --reload
```
服务将在 http://localhost:8000 启动

### 前端服务

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
# 使用淘宝镜像源安装依赖（推荐）
npm install --registry=https://registry.npmmirror.com
```

3. 配置环境变量：
   - 复制 `.env.example` 到 `.env`
   - 确保 `VITE_API_BASE_URL` 指向正确的后端地址

4. 运行开发服务器：
```bash
npm run dev
```
前端将在 http://localhost:3000 启动

### Docker 部署

使用 Docker 可以更便捷地部署后端、前端和数据库服务，无需手动安装各项依赖和配置环境。

确保您已经安装了 Docker 和 Docker Compose。

1. 构建 Docker 镜像：
   在项目根目录（`hot-news-app/`）下执行以下命令：
   ```bash
   docker compose build
   ```
   这将根据 `Dockerfile` 文件构建后端和前端的 Docker 镜像。

2. 配置环境变量：
   复制 `.env.example` 到 `.env`：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件，修改数据库连接、知乎 Cookie、和风天气 API Key 等配置。**请注意，如果您的后端和数据库运行在 Docker 容器中，数据库的 `DATABASE_URL` 可能需要修改为指向 Docker 网络中的数据库服务名称，例如 `mysql+pymysql://root:password@db/hot_news`（假设数据库服务的名称为 `db`）。**

3. 运行 Docker Compose：
   在项目根目录（`hot-news-app/`）下执行以下命令启动所有服务：
   ```bash
   docker compose up -d
   ```
   `-d` 参数表示在后台运行服务。

4. 访问应用：
   - 后端 API 将在 http://localhost:8000 可访问。
   - 前端应用将在 http://localhost:3000 可访问。

5. 停止服务：
   在项目根目录（`hot-news-app/`）下执行以下命令停止所有服务：
   ```bash
   docker compose down
   ```
   这将停止并移除所有由 Docker Compose 启动的容器、网络和卷。

**注意事项：**

- 首次运行时需要下载镜像和构建镜像，可能需要一些时间，请耐心等待。
- 数据库数据将保存在 Docker 卷中，即使容器被停止或移除，数据也会保留。
- 如果您修改了后端或前端代码，需要重新构建镜像并重启服务 (`docker compose build` 和 `docker compose up -d`)。
- 确保您的防火墙允许访问 8000 和 3000 端口。

## API 文档

启动后端服务后访问：http://localhost:8000/docs 查看完整的 API 文档

主要接口：
- GET /api/v1/hot-topics - 获取所有热搜话题
- GET /api/v1/hot-topics/{source} - 获取指定来源的热搜话题

## 注意事项

1. 知乎爬虫需要配置 Cookie 才能正常工作，请在 `.env` 文件中设置：
```
ZHIHU_COOKIE=your_cookie_here
```

2. 建议配置代理 IP 池来避免被封禁

3. 默认每 30 分钟更新一次数据，可在配置文件中修改更新间隔

4. 确保 MySQL 服务已启动且配置正确

5. Windows 用户注意事项：
   - 如果使用 PowerShell 遇到执行策略限制，请以管理员身份运行 PowerShell 并执行：
     ```powershell
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
   - 或者使用 CMD 来运行命令

6. 网络问题解决方案：
   - 如果遇到 pip 安装超时，请使用国内镜像源
   - 如果遇到 npm 安装慢，请使用淘宝镜像源
   - 如果仍然遇到问题，可以尝试使用代理或 VPN

7. 环境变量配置说明：
   - 必填项：
     - `DATABASE_URL`：数据库连接 URL
     - `ZHIHU_COOKIE`：知乎 Cookie
   - 可选项：
     - `CRAWL_INTERVAL`：爬虫更新间隔
     - `USER_AGENT`：用户代理
     - `HTTP_PROXY`/`HTTPS_PROXY`：代理服务器
8. 清理项目缓存：
   - 如果遇到代码更新后不生效的问题，可以尝试清理 Python 缓存：
     ```bash
     # Windows (CMD)
     for /d /r . %d in (__pycache__) do @if exist "%d" rd /s/q "%d"
     for /r . %f in (*.pyc) do @if exist "%f" del /f /q "%f"

     # Windows (PowerShell)
     Remove-Item -Path ".\app\**\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
     Remove-Item -Path ".\**\*.pyc" -Recurse -Force -ErrorAction SilentlyContinue

     # Linux/Mac
     find . -type d -name "__pycache__" -exec rm -r {} +
     find . -name "*.pyc" -delete
     ```     

## 开发说明

1. 后端开发：
   - 遵循 PEP 8 编码规范
   - 使用 Type Hints
   - 编写单元测试

2. 前端开发：
   - 使用 TypeScript 进行开发
   - 遵循 Vue 3 组合式 API 风格
   - 使用 ESLint 和 Prettier 保持代码风格一致

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 