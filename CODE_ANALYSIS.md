# 代码分析文档

## v0.4.0

### 管理后台接口

- `backend/app/main.py`：新增 `ArticleIn` 请求模型。
- `POST /api/admin/articles`：根据标题、摘要、正文、标签、日期和阅读时长创建文章，并初始化点赞、收藏、点踩计数。
- `PUT /api/admin/articles/{article_id}`：更新文章内容和标签。
- `DELETE /api/admin/articles/{article_id}`：删除文章，关联评论和互动计数随文章删除。
- `_generate_article_id`：根据标题生成文章 ID；中文标题无法生成英文 slug 时使用 `article-YYYYMMDD` 并自动处理重复。

### 前端管理页

- `frontend/src/App.jsx`：新增导航项“管理”和 `AdminWorkspace` 组件。
- 管理表单支持文章标题、摘要、正文、标签、日期、阅读时长。
- 已有文章列表支持编辑和删除；保存后调用 `/api/articles` 重新同步文章、评论和互动计数。
- `frontend/src/styles.css`：新增管理后台表单、按钮、文章管理列表和响应式布局样式。

### 文档整理

- `.gitignore`：新增 `.external/`，避免把外部小游戏仓库误提交到博客仓库。
- `docs/archive/DOCKER_DESKTOP_SETUP.md`、`docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`、`docs/archive/个人博客搭建流程.md`：归档阶段性文档。
- `README.md`、`NEXT_STEPS.md`：更新当前状态和下一步计划。

### 小游戏仓库

- 外部仓库 `card-war-made-by-class-3` 的 `css/style.css` 已新增 `#game-screen` 纵向滚动能力。
- 提交号：`9c63c50 fix: allow scrolling in game screen`。

## v0.3.0

### PostgreSQL 与 Docker

- `docker-compose.yml`：新增 PostgreSQL 16 容器，配置数据库名、账号、密码、端口映射、持久化 volume 和健康检查。
- `.env.example`：更新 `DATABASE_URL`，使用 `postgresql+psycopg://felix_blog:felix_blog_dev@localhost:5432/felix_blog`。
- `backend/requirements.txt`：新增 `sqlalchemy` 和 `psycopg[binary]`。

### 后端持久化

- `backend/app/database.py`：集中管理 SQLAlchemy engine、SessionLocal、Base、建表和 FastAPI DB 依赖。
- `backend/app/models.py`：新增用户、文章、标签、文章标签关联、评论和互动计数模型。
- `backend/app/seed.py`：新增 3 篇示例文章和默认互动计数的初始化逻辑。
- `backend/app/main.py`：启动时自动建表和写入种子数据；文章列表、文章搜索、评论提交、互动提交全部改为数据库读写。

### 前端联调

- `frontend/src/App.jsx`：启动时从 `/api/articles` 读取评论和互动计数；发表评论调用 `/comments` 接口；点赞、收藏、点踩调用 `/reaction` 接口并同步计数。
- `frontend/src/styles.css`：补充评论作者和内容的显示样式。

### 文档

- `DATABASE.md`：记录本地数据库启动、连接信息、表结构、接口行为和验证命令。
- `README.md`：加入数据库启动步骤和 v0.4.0 下一步方向。
- `NEXT_STEPS.md`：更新项目状态和下一步计划。

## v0.2.3

### Git 代理配置

- 当前仓库的 Git local config 已设置 `http.proxy` 和 `https.proxy` 为 `http://127.0.0.1:7897`，让 Git for Windows 通过 Clash 访问 GitHub。
- 该配置位于 `.git/config`，不会被提交到远程仓库。
- 使用代理后已成功执行 `git ls-remote` 和 `git push`。

### 小游戏响应式嵌入

- `frontend/src/App.jsx`：调整 `GameWorkspace` 结构，把说明和按钮集中为控制条，把 iframe 放到全宽游戏区域，避免游戏被右侧说明栏压缩。
- `frontend/src/styles.css`：将 `.game-layout` 改为单列布局，`.game-stage` 使用 `clamp(560px, calc(100vh - 210px), 900px)` 根据浏览器高度自适应，移动端使用 `72vh` 和 `500px` 最小高度。
- 更新后的小游戏页面自身使用 `#game-container { width: 100vw; height: 100vh; }`，因此博客只需要给 iframe 提供稳定、宽裕的视口。

## v0.2.2

### 环境准备文档

- `DOCKER_DESKTOP_SETUP.md`：新增 Docker Desktop 安装与验证指南，覆盖 WSL/Ubuntu、Docker Desktop、Docker Compose、`hello-world` 验证和后续 PostgreSQL 准备。
- `GITHUB_PUSH_TROUBLESHOOTING.md`：新增 GitHub 推送问题排查文档，记录 PowerShell 可访问 GitHub、Git for Windows 连接超时的现象，并给出代理、GitHub Desktop、GitHub API 三类替代方案。
- `NEXT_STEPS.md`：更新当前阻塞点，把 Docker 安装和 GitHub 推送排查列为 v0.3.0 前置事项。
- `README.md`：增加两份环境文档入口。

## v0.2.1

### 下一步计划文档

- `NEXT_STEPS.md`：新增下一步开发计划，说明当前状态、GitHub 推送阻塞点、推荐的 v0.3.0 数据持久化目标，以及用户需要做和我可以辅助完成的事项。
- `README.md`：更新目录结构、GitHub 连接状态和下一步开发入口。
- `CHANGELOG.md`：记录本次文档更新，方便后续验收时追踪版本变化。

## v0.2.0

### 小游戏集成

- `frontend/src/data.js`：为 `gameModule` 增加 `playUrl`，指向 `https://firefelixfu026.github.io/card-war-made-by-class-3/`，并把状态从“待集成”改为“已嵌入”。
- `frontend/src/App.jsx`：在 `GameWorkspace` 中使用 `iframe` 直接嵌入小游戏页面，同时增加刷新游戏、新窗口打开和查看仓库按钮。
- `frontend/src/styles.css`：调整游戏区域布局，使用固定最小高度保证 iframe 有足够操作空间，并适配移动端。
- `backend/app/main.py`：更新 `/api/game/card-war` 返回结构，增加 `playUrl` 和 `embedded` 状态，方便后续前端改为从接口读取游戏配置。

## v0.1.0

### 前端

- `frontend/src/App.jsx`：实现博客 MVP 的主界面，包括个人信息、文章搜索、标签筛选、互动按钮、评论输入、AI 内容入口和小游戏入口。
- `frontend/src/data.js`：集中存放 MVP 阶段的个人信息、文章、AI 新闻、小游戏仓库信息等静态数据，后续可替换为 API 数据。
- `frontend/src/styles.css`：实现响应式布局、导航、文章列表、状态面板和表单样式。
- `frontend/src/main.jsx`：React 应用入口。

### 后端

- `backend/app/main.py`：提供 FastAPI 应用和 MVP 接口，包括健康检查、个人信息、文章列表、文章详情、评论、互动、AI 新闻和小游戏信息。

### 文档

- `需求.md`：系统化整理用户需求、技术路线、功能优先级、接口规划和账号需求。
- `README.md`：说明项目目标、目录结构和本地启动方式。
- `CHANGELOG.md`：记录版本更新内容。

### 后续需要补充

- PostgreSQL 数据模型和迁移脚本。
- 登录注册和 GitHub OAuth。
- Docker Compose。
- GitHub Actions。
- 云服务器部署文档。
