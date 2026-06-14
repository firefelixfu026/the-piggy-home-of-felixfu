# Docker Compose 一键启动说明

当前项目已支持通过 Docker Compose 同时启动：

- PostgreSQL 数据库
- FastAPI 后端
- React 前端静态站点
- Nginx 前端静态服务和 `/api` 反向代理

统一访问入口：

```text
http://127.0.0.1:8080
```

后端调试入口：

```text
http://127.0.0.1:8000/api/health
```

## 1. 首次启动前准备

确认 Docker Desktop 已启动。

如果 Docker 命令找不到 credential helper，先在当前 PowerShell 执行：

```powershell
$env:Path = 'C:\Program Files\Docker\Docker\resources\bin;' + $env:Path
```

如果拉取 Docker Hub 镜像超时，并且你正在使用 Clash `127.0.0.1:7897`，在当前 PowerShell 执行：

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
$env:NO_PROXY='localhost,127.0.0.1'
```

## 2. 配置本地环境变量

如果只测试文章、评论、后台和数据库，可以不配置 GitHub OAuth。

如果要测试 GitHub 登录，建议复制 `.env.example` 为 `.env`：

```powershell
Copy-Item .env.example .env
```

然后编辑 `.env`，填写：

```text
AUTH_SECRET=换成你自己的随机字符串
GITHUB_CLIENT_ID=你的 GitHub OAuth Client ID
GITHUB_CLIENT_SECRET=你的 GitHub OAuth Client Secret
GITHUB_OAUTH_CALLBACK_URL=http://127.0.0.1:8000/api/auth/github/callback
GITHUB_ADMIN_LOGINS=你的 GitHub 登录名
FRONTEND_ORIGIN=http://127.0.0.1:8080
```

`.env` 已被 `.gitignore` 忽略，不会提交到 GitHub。

## 3. 一键启动

在项目根目录执行：

```powershell
docker compose up -d --build
```

如果当前 PowerShell 没有把 Docker 加入 PATH，可以使用完整路径：

```powershell
& 'C:\Program Files\Docker\Docker\resources\bin\docker.exe' compose up -d --build
```

首次启动会下载 `python`、`node`、`nginx`、`postgres` 镜像，并安装前后端依赖，耗时会比较久。后续启动会复用缓存。

## 4. 查看服务状态

```powershell
docker compose ps
```

期望看到：

- `felixfu_blog_postgres`：healthy
- `felixfu_blog_backend`：healthy
- `felixfu_blog_frontend`：Up

## 5. 验证服务

前端：

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8080' -UseBasicParsing
```

前端代理到后端：

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8080/api/health'
```

后端直连：

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health'
```

期望返回：

```text
status: ok
version: 0.8.0
```

## 6. 停止服务

停止容器但保留数据库数据：

```powershell
docker compose down
```

停止容器并删除数据库 volume：

```powershell
docker compose down -v
```

删除 volume 会清空本地 PostgreSQL 数据，包括文章、评论和用户。

## 7. 常见问题

### 端口被占用

如果 `8000` 或 `8080` 已被占用，先找出占用进程：

```powershell
Get-NetTCPConnection -LocalPort 8000,8080 -ErrorAction SilentlyContinue
```

如果是之前手动启动的后端或前端，停止它后再运行 Docker Compose。

### 拉取镜像超时

先确认 Clash 正在运行，再设置：

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
$env:NO_PROXY='localhost,127.0.0.1'
```

然后重新执行：

```powershell
docker compose up -d --build
```

### GitHub 登录后没有管理员权限

检查 `.env`：

```text
GITHUB_ADMIN_LOGINS=你的 GitHub 登录名
```

修改后重新创建后端和前端容器：

```powershell
docker compose up -d --force-recreate backend frontend
```

### OAuth 回调 URL

当前 Docker Compose 配置为了兼容已经创建的 GitHub OAuth App，仍使用后端直连回调：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

授权完成后，后端会把浏览器带回：

```text
http://127.0.0.1:8080
```
