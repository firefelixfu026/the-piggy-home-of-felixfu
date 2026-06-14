# 代码分析文档

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

