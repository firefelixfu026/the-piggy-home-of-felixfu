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
├── docker-compose.yml     # PostgreSQL 本地数据库
├── 需求.md                # 系统化需求说明
├── NEXT_STEPS.md          # 下一步开发计划
├── DATABASE.md            # 数据库和持久化说明
├── DOCKER_DESKTOP_SETUP.md # Docker Desktop 安装与验证
├── GITHUB_PUSH_TROUBLESHOOTING.md # GitHub 推送排查
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

## 下一步

v0.3.0 已完成 PostgreSQL 数据持久化。下一步建议推进 v0.4.0 文章管理后台，支持管理员发布、编辑、删除文章。详细计划见 [NEXT_STEPS.md](./NEXT_STEPS.md)。

开始 v0.3.0 前，需要先完成 Docker Desktop 安装与验证，步骤见 [DOCKER_DESKTOP_SETUP.md](./DOCKER_DESKTOP_SETUP.md)。

当前 Git for Windows 推送 GitHub 仍有网络问题，排查与替代方案见 [GITHUB_PUSH_TROUBLESHOOTING.md](./GITHUB_PUSH_TROUBLESHOOTING.md)。

## GitHub 连接

当前项目已绑定 GitHub 远程仓库：

- 仓库地址：`https://github.com/firefelixfu026/the-piggy-home-of-felixfu`
- 用户名：`felixfu026`

后续如果要继续完成 GitHub OAuth 登录和 GitHub Actions 部署，还需要：

- GitHub OAuth App 的 Client ID 和 Client Secret。
- GitHub Actions 部署所需的服务器 SSH 信息。
- 云服务器公网 IP、SSH 用户名、部署目录和域名信息。
