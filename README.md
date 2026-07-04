# FelixFu 个人博客

[![CI](https://github.com/firefelixfu026/the-piggy-home-of-felixfu/actions/workflows/ci.yml/badge.svg)](https://github.com/firefelixfu026/the-piggy-home-of-felixfu/actions/workflows/ci.yml)

这是付江樊的综合型个人博客项目，目标是从 6 小时内可展示 MVP 起步，逐步扩展为支持文章发布、搜索、评论、点赞、收藏、点踩、管理员登录、GitHub 登录、AI 自动化内容、小游戏和云服务器部署的完整前后端分离系统。

## 技术栈

- 前端：React + Vite
- 后端：FastAPI
- 数据库：PostgreSQL
- 鉴权：邮箱密码 + GitHub OAuth + HS256 token
- 自动化：GitHub Actions CI
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
├── DATABASE_BACKUP.md     # 线上数据库备份和恢复指南
├── DOCKER_COMPOSE.md      # Docker Compose 一键启动说明
├── GITHUB_OAUTH_APP_SETUP.md # GitHub OAuth App 创建指南
├── GITHUB_ACTIONS_DEPLOYMENT.md # GitHub Actions 自动部署指南
├── CLOUD_SERVER_DOMAIN_PREP.md # 云服务器和域名购买准备指南
├── CLOUD_SERVER_DEPLOYMENT.md # 云服务器部署执行指南
├── SERVER_OPERATIONS.md   # 服务器日常运维指南
├── docs/archive/          # 已归档的阶段性文档
├── CHANGELOG.md           # 版本日志
├── CODE_ANALYSIS.md       # 代码分析文档
└── README.md              # 项目说明
```

## 线上地址

当前正式访问地址：

```text
https://www.felixfu.xyz
```

部署状态：

- 阿里云中国香港 Ubuntu 22.04
- Docker Compose 运行前端、后端和 PostgreSQL
- Nginx 反向代理
- Certbot / Let''s Encrypt HTTPS
- GitHub OAuth 登录已成功

## 本地启动

推荐优先使用 Docker Compose，一条命令同时启动 PostgreSQL、FastAPI 后端和 React 前端静态站点。

```powershell
cd E:\FelixFu\document\网站\FelixFu
docker compose up -d --build
```

统一访问地址：

- 前端：`http://127.0.0.1:8080`
- 后端健康检查：`http://127.0.0.1:8000/api/health`
- 前端代理健康检查：`http://127.0.0.1:8080/api/health`

如果 PowerShell 找不到 `docker` 命令，可以先执行：

```powershell
$env:Path = 'C:\Program Files\Docker\Docker\resources\bin;' + $env:Path
```

如果需要 GitHub 登录，先复制 `.env.example` 为 `.env` 并填写 GitHub OAuth 信息：

```powershell
Copy-Item .env.example .env
```

完整启动、停止、验证和常见问题见 [DOCKER_COMPOSE.md](./DOCKER_COMPOSE.md)。

互动说明：点赞、收藏、点踩和“？”需要先登录；每个账号对同一篇文章的同一种互动只能记录一次。评论最多 300 字，文章页会按评论显示长度分页。

如果只想手动启动开发服务，可以使用下面的方式。

数据库：

```powershell
docker compose up -d postgres
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

手动开发访问地址：

- 前端：`http://127.0.0.1:5173`
- 后端健康检查：`http://127.0.0.1:8000/api/health`
- 数据库说明：见 [DATABASE.md](./DATABASE.md)

## 已集成模块

- 决斗小游戏：博客内通过 iframe 嵌入 `https://firefelixfu026.github.io/card-war-made-by-class-3/`，同时保留新窗口打开和源码仓库入口。
- 登录鉴权：导航栏“登录”页支持 GitHub OAuth、带初始化密钥的管理员初始化和邮箱密码登录，登录状态会保存到浏览器本地。
- 管理后台：只有管理员登录后才显示“管理”入口；后台支持发布、编辑、删除文章，并集中查看、刷新、删除评论，后台操作需要管理员 token。
- 数据持久化：文章、评论、账号级点赞、收藏、点踩和“？”互动写入 PostgreSQL，刷新网页不会重复计数。
- 自动测试：GitHub Actions 每次 push/PR 自动检查后端编译、前端构建和 Docker Compose 配置。

## 管理员登录

首次使用新的本地数据库时：

1. 启动 PostgreSQL 和 FastAPI 后端。
2. 在 `.env` 中设置 `ADMIN_SETUP_TOKEN`，这个值只给站长自己使用。
3. 打开前端。Docker 版使用 `http://127.0.0.1:8080`，手动开发版使用 `http://127.0.0.1:5173`。
4. 进入“登录”页，选择“初始化管理员”，填写邮箱、密码和初始化密钥。
5. 初始化成功后进入“管理”页发布、编辑或删除文章。

如果已经初始化过管理员，直接在“登录”页使用 GitHub 或邮箱密码登录。公开站点没有正确初始化密钥时，无法创建管理员账号。

## GitHub OAuth 设置

完整创建步骤见 [GITHUB_OAUTH_APP_SETUP.md](./GITHUB_OAUTH_APP_SETUP.md)。

在 GitHub 创建 OAuth App 时，本地开发建议填写：

```text
Homepage URL: http://127.0.0.1:8080
Authorization callback URL: http://127.0.0.1:8000/api/auth/github/callback
```

然后把凭据写入本地环境变量或 `.env`：

```text
GITHUB_CLIENT_ID=你的 Client ID
GITHUB_CLIENT_SECRET=你的 Client Secret
GITHUB_OAUTH_CALLBACK_URL=http://127.0.0.1:8000/api/auth/github/callback
GITHUB_ADMIN_LOGINS=你的 GitHub 登录名
```

`GITHUB_ADMIN_LOGINS` 用逗号分隔。匹配到的 GitHub 用户登录后会获得管理员权限；未匹配的新 GitHub 用户默认是 `reader`。

## 上线后运维

当前已补充：

- [DATABASE_BACKUP.md](./DATABASE_BACKUP.md)：数据库备份、恢复、自动备份和备份检查。
- [SERVER_OPERATIONS.md](./SERVER_OPERATIONS.md)：服务器更新、日志、重启、Nginx、HTTPS、磁盘和故障排查。

建议上线后先在服务器执行一次数据库备份，并测试 Certbot 自动续期。

## 下一步

v0.8.0 已完成 GitHub Actions 自动测试。v0.8.1 已补充本地启动说明和云服务器部署文档。

下一步建议进入 v0.9.0：使用阿里云准备云服务器部署、Nginx、域名和 HTTPS。

当前云平台选择：阿里云。服务器已购买：中国香港 Ubuntu 22.04，公网 IP：`47.242.176.227`。正式域名已上线：`https://www.felixfu.xyz`。HTTPS 已配置，GitHub OAuth 登录已成功；公网 IP `http://47.242.176.227` 仍可作为服务器访问参考。

执行顺序建议：

1. 本地执行 `docker compose up -d --build`，确认 `http://127.0.0.1:8080` 可访问。
2. 打开 GitHub 仓库的 Actions 页面，确认 CI 通过。
3. 购买或准备云服务器和域名，购买前阅读 [CLOUD_SERVER_DOMAIN_PREP.md](./CLOUD_SERVER_DOMAIN_PREP.md)。
4. 按 [CLOUD_SERVER_DEPLOYMENT.md](./CLOUD_SERVER_DEPLOYMENT.md) 执行服务器部署。
5. 上线前重新生成 GitHub OAuth Client Secret，并更新正式回调地址。

云服务器部署需要的信息：

- 云服务器公网 IP、SSH 用户名和部署目录。
- 域名和 DNS 管理平台，如果已有。
- GitHub OAuth 的正式线上配置。

详细计划见 [NEXT_STEPS.md](./NEXT_STEPS.md)。

## GitHub 连接

当前项目已绑定 GitHub 远程仓库：

- 仓库地址：`https://github.com/firefelixfu026/the-piggy-home-of-felixfu`
- 用户名：`felixfu026`

后续如果要继续完成 GitHub Actions 部署和云服务器上线，还需要：

- GitHub Actions 部署所需的服务器 SSH 信息。
- 云服务器公网 IP、SSH 用户名、部署目录和域名信息。
