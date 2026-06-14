# FelixFu 个人博客

这是付江樊的综合型个人博客项目，目标是从 6 小时内可展示 MVP 起步，逐步扩展为支持文章发布、搜索、评论、点赞、收藏、点踩、GitHub 登录、AI 自动化内容、小游戏和云服务器部署的完整前后端分离系统。

## 技术栈

- 前端：React + Vite
- 后端：FastAPI
- 数据库：PostgreSQL，MVP 阶段暂未接入
- 自动化：GitHub Actions，后续接入
- 部署：云服务器 + Docker + Nginx，后续接入

## 目录结构

```text
.
├── frontend/              # React 前端
├── backend/               # FastAPI 后端
├── 需求.md                # 系统化需求说明
├── CHANGELOG.md           # 版本日志
├── CODE_ANALYSIS.md       # 代码分析文档
└── README.md              # 项目说明
```

## 本地启动

前端：

```powershell
cd frontend
npm.cmd install
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

后端：

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

访问地址：

- 前端：`http://127.0.0.1:5173`
- 后端健康检查：`http://127.0.0.1:8000/api/health`

## 已集成模块

- 决斗小游戏：博客内通过 iframe 嵌入 `https://firefelixfu026.github.io/card-war-made-by-class-3/`，同时保留新窗口打开和源码仓库入口。

## GitHub 连接

当前项目还没有绑定 GitHub 远程仓库。后续如果要满足“每次版本更新后推送 GitHub”的要求，需要提供：

- GitHub 仓库地址
- 是否使用 GitHub OAuth 登录
- GitHub OAuth App 的 Client ID 和 Client Secret
- GitHub Actions 部署所需的服务器 SSH 信息
