# FelixFu 个人博客

这是付江樊的综合型个人博客项目，目标是从 6 小时内可展示 MVP 起步，逐步扩展为支持文章发布、搜索、评论、点赞、收藏、点踩、GitHub 登录、AI 自动化内容、小游戏和云服务器部署的完整前后端分离系统。

## 技术栈

- 前端：React + Vite
- 后端：FastAPI
- 数据库：PostgreSQL
- 自动化：GitHub Actions，后续接入
- 部署：云服务器 + Docker + Nginx，后续接入

## 目录结构

```text
.
├── frontend/              # React 前端
├── backend/               # FastAPI 后端
├── docker-compose.yml     # PostgreSQL 本地数据库
├── 需求.md                # 系统化需求说明
├── NEXT_STEPS.md          # 下一步开发计划
├── DATABASE.md            # 数据库和持久化说明
├── docs/archive/          # 已归档的阶段性文档
├── CHANGELOG.md           # 版本日志
├── CODE_ANALYSIS.md       # 代码分析文档
└── README.md              # 项目说明
```

## 本地启动

数据库：

```powershell
docker compose up -d postgres
```

如果 PowerShell 找不到 `docker` 命令，可以先执行：

```powershell
$env:Path = 'C:\Program Files\Docker\Docker\resources\bin;' + $env:Path
```

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
- 数据库说明：见 [DATABASE.md](./DATABASE.md)

## 已集成模块

- 决斗小游戏：博客内通过 iframe 嵌入 `https://firefelixfu026.github.io/card-war-made-by-class-3/`，同时保留新窗口打开和源码仓库入口。
- 管理后台：导航栏“管理”页支持发布、编辑、删除文章。
- 数据持久化：文章、评论、点赞、收藏、点踩写入 PostgreSQL。

## 下一步

v0.4.0 已完成文章管理后台。下一步建议推进 v0.5.0 登录鉴权，给管理后台加管理员保护。详细计划见 [NEXT_STEPS.md](./NEXT_STEPS.md)。

Docker 安装和 GitHub 推送排查文档已归档到 `docs/archive/`。

## GitHub 连接

当前项目已绑定 GitHub 远程仓库：

- 仓库地址：`https://github.com/firefelixfu026/the-piggy-home-of-felixfu`
- 用户名：`felixfu026`

后续如果要继续完成 GitHub OAuth 登录和 GitHub Actions 部署，还需要：

- GitHub OAuth App 的 Client ID 和 Client Secret。
- GitHub Actions 部署所需的服务器 SSH 信息。
- 云服务器公网 IP、SSH 用户名、部署目录和域名信息。
