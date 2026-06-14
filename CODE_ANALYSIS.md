# 代码分析文档

## v0.7.0

### Docker Compose 一键启动

- `docker-compose.yml`：新增 `backend` 和 `frontend` 服务，保留 `postgres` 服务。
- `backend`：使用 `backend/Dockerfile` 构建 FastAPI 镜像，容器内监听 `0.0.0.0:8000`，通过 `postgres:5432` 访问数据库。
- `frontend`：使用 `frontend/Dockerfile` 多阶段构建，第一阶段用 Node/Vite 构建，第二阶段用 Nginx 服务静态文件。
- `frontend/nginx.conf`：`/api/` 反向代理到 `http://backend:8000/api/`，其余路径走 SPA fallback。
- `backend` healthcheck：访问容器内 `http://127.0.0.1:8000/api/health`。
- `frontend` 依赖 `backend` healthy 后启动。
- `.dockerignore`、`backend/.dockerignore`、`frontend/.dockerignore`：排除 `node_modules`、`dist`、虚拟环境、缓存和密钥文件。

### 访问方式

- Docker 版前端统一入口：`http://127.0.0.1:8080`。
- 后端调试入口：`http://127.0.0.1:8000/api/health`。
- PostgreSQL 仍映射本地 `5432`。
- GitHub OAuth 本地回调仍使用 `http://127.0.0.1:8000/api/auth/github/callback`，回调后跳回 `FRONTEND_ORIGIN=http://127.0.0.1:8080`。

### 验证结果

- `docker compose config` 通过。
- `docker compose up -d --build` 构建并启动成功。
- `docker compose ps` 显示 `postgres` 和 `backend` healthy，`frontend` running。
- `http://127.0.0.1:8080` 返回 200。
- `http://127.0.0.1:8080/api/health` 返回 `version: 0.7.0`。
- `http://127.0.0.1:8000/api/health` 返回 `version: 0.7.0`。
- Docker 版 `GET /api/auth/github/start` 能正确跳转到 GitHub 授权页。

## v0.6.0

### GitHub OAuth 后端

- `backend/app/github_oauth.py`：新增 GitHub OAuth 专用模块，负责生成授权 URL、用 code 换取 access token、读取 GitHub 用户资料和主邮箱。
- `backend/app/auth.py`：新增 `create_oauth_state` 和 `verify_oauth_state`，使用 HMAC 签名 state，并设置默认 10 分钟有效期。
- `backend/app/main.py`：新增 `GET /api/auth/github/start` 和 `GET /api/auth/github/callback`。
- `_upsert_github_user`：根据 GitHub ID 查找用户；如果不存在则按邮箱绑定已有用户；否则创建新用户。
- `_is_configured_github_admin`：读取 `GITHUB_ADMIN_LOGINS` 和 `GITHUB_ADMIN_EMAILS`，匹配到的 GitHub 用户获得管理员角色。
- `_frontend_auth_redirect`：OAuth 成功或失败后重定向回前端 hash，成功时带本站 token，失败时带错误信息。

### GitHub OAuth 前端

- `frontend/src/App.jsx`：登录页新增“使用 GitHub 登录”按钮，指向 `/api/auth/github/start`。
- `frontend/src/App.jsx`：新增 hash 回调解析逻辑，识别 `#auth=github&token=...` 后保存 token 并进入管理页。
- `frontend/src/styles.css`：新增 GitHub 登录按钮和登录分隔线样式。

### 配置

- `.env.example`：新增 `GITHUB_OAUTH_CALLBACK_URL`、`GITHUB_ADMIN_LOGINS`、`GITHUB_ADMIN_EMAILS`。
- 本地 GitHub OAuth App 推荐回调地址：`http://127.0.0.1:8000/api/auth/github/callback`。

## v0.5.0

### 登录鉴权

- `backend/app/auth.py`：新增密码哈希、密码校验、HS256 token 签发、token 校验、当前用户依赖和管理员依赖。
- `backend/app/models.py`：`User` 模型新增 `password_hash` 字段，用于邮箱密码登录。
- `backend/app/database.py`：启动时检测旧版 `users` 表，如果缺少 `password_hash` 字段会自动执行轻量迁移。
- `backend/app/main.py`：新增 `RegisterIn`、`LoginIn` 请求模型，以及 `/api/auth/register`、`/api/auth/login`、`/api/auth/me`。
- `POST /api/admin/articles`、`PUT /api/admin/articles/{article_id}`、`DELETE /api/admin/articles/{article_id}`：全部增加 `require_admin` 依赖。

### 前端登录和后台保护

- `frontend/src/App.jsx`：新增登录状态、token 本地保存、`/api/auth/me` 校验、登录/初始化管理员流程和退出登录。
- `LoginWorkspace`：新增“登录”和“初始化管理员”两种模式。
- `AdminWorkspace`：新增管理员会话条，未登录时不再显示后台表单。
- 后台文章创建、编辑、删除请求会带 `Authorization: Bearer <token>`。
- `frontend/src/styles.css`：新增登录页、模式切换、管理员会话条和移动端导航样式。

### 小游戏仓库

- 外部仓库 `card-war-made-by-class-3` 的 `js/main.js` 新增规则页返回来源状态。
- 从开始页进入规则页会返回开始页，从局内进入规则页会返回局内。
- 提交号：`4a65677 fix: return to game after viewing rules`。

### 验证结果

- `python -m compileall backend\app` 通过。
- `npm.cmd run build` 通过。
- `/api/health` 返回 `version: 0.5.0`。
- 未登录访问后台文章接口返回 `401`。
- 管理员注册/登录、`/api/auth/me`、带 token 的文章新增/编辑/删除冒烟测试通过。

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
