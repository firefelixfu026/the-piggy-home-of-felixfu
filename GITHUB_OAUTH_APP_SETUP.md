# GitHub OAuth App 创建与本地配置指南

本文档用于给当前博客项目创建 GitHub OAuth App，并把 GitHub 登录接入本地开发环境。

官方参考：

- GitHub Docs: <https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app>

## 1. 你需要准备什么

你需要：

- 一个可登录的 GitHub 账号。
- 本地博客前端地址：`http://127.0.0.1:5173`
- 本地博客后端地址：`http://127.0.0.1:8000`
- 本项目 GitHub OAuth 回调地址：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

## 2. 创建 OAuth App

1. 打开 GitHub：<https://github.com>
2. 点击右上角头像。
3. 进入 `Settings`。
4. 在左侧菜单底部进入 `Developer settings`。
5. 进入 `OAuth Apps`。
6. 点击 `New OAuth App`。
7. 填写表单：

```text
Application name:
FelixFu Blog Local

Homepage URL:
http://127.0.0.1:5173

Application description:
FelixFu personal blog local development login

Authorization callback URL:
http://127.0.0.1:8000/api/auth/github/callback
```

8. 点击 `Register application`。

## 3. 获取 Client ID 和 Client Secret

创建成功后，GitHub 会进入这个 OAuth App 的详情页。

你需要复制：

- `Client ID`
- `Client Secret`

`Client Secret` 默认不会直接显示，需要点击 `Generate a new client secret` 创建。

注意：

- `Client ID` 可以放在本地环境变量里。
- `Client Secret` 是密钥，不要提交到 GitHub。
- 不要把真实密钥写进 `README.md`、`NEXT_STEPS.md`、`CHANGELOG.md` 或任何会提交的文件。

## 4. 配置本地后端环境变量

当前项目后端读取的是系统环境变量。`.env.example` 只是模板，直接修改 `.env.example` 不会让后端自动读取。

在启动后端的同一个 PowerShell 窗口里执行：

```powershell
$env:GITHUB_CLIENT_ID="粘贴你的 Client ID"
$env:GITHUB_CLIENT_SECRET="粘贴你的 Client Secret"
$env:GITHUB_OAUTH_CALLBACK_URL="http://127.0.0.1:8000/api/auth/github/callback"
$env:GITHUB_ADMIN_LOGINS="你的 GitHub 登录名"
```

然后启动后端：

```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

`GITHUB_ADMIN_LOGINS` 决定哪些 GitHub 用户登录后是管理员。多个用户用英文逗号分隔：

```powershell
$env:GITHUB_ADMIN_LOGINS="user1,user2"
```

如果你不确定自己的 GitHub 登录名，打开 GitHub 个人主页，看 URL：

```text
https://github.com/你的登录名
```

## 5. 启动前端并测试

启动前端：

```powershell
cd frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

打开：

```text
http://127.0.0.1:5173
```

测试流程：

1. 进入博客左侧导航的“登录”页。
2. 点击“使用 GitHub 登录”。
3. GitHub 会显示授权页面。
4. 点击授权。
5. 浏览器会回到博客前端。
6. 如果 `GITHUB_ADMIN_LOGINS` 配置正确，会进入“管理”页并拥有文章管理权限。

## 6. 常见问题

### GitHub 登录后提示 `GITHUB_CLIENT_ID is not configured`

说明后端启动时没有读到环境变量。

处理方式：

1. 停止后端。
2. 在同一个 PowerShell 窗口重新设置 `$env:GITHUB_CLIENT_ID` 和 `$env:GITHUB_CLIENT_SECRET`。
3. 重新启动后端。

### GitHub 提示 callback URL 不匹配

检查 GitHub OAuth App 里的 `Authorization callback URL` 是否完全等于：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

协议、IP、端口、路径都必须一致。

### GitHub 登录成功但不能进入管理后台

通常是 `GITHUB_ADMIN_LOGINS` 没有填对。

检查你的 GitHub 登录名是否和环境变量一致：

```powershell
$env:GITHUB_ADMIN_LOGINS="你的 GitHub 登录名"
```

然后重启后端并重新登录。

### 已经用邮箱初始化过管理员，GitHub 还能绑定吗

可以。如果 GitHub 主邮箱和本地管理员邮箱一致，后端会把 GitHub 账号绑定到已有用户。

如果邮箱不一致，就使用 `GITHUB_ADMIN_LOGINS` 指定你的 GitHub 登录名，让 GitHub 登录后的用户成为管理员。

## 7. 上线部署时要改什么

上线后不能继续使用 `127.0.0.1` 作为 OAuth 回调。

假设你的正式域名是：

```text
https://example.com
```

则 GitHub OAuth App 建议改成：

```text
Homepage URL:
https://example.com

Authorization callback URL:
https://example.com/api/auth/github/callback
```

同时服务器环境变量也要改：

```text
FRONTEND_ORIGIN=https://example.com
GITHUB_OAUTH_CALLBACK_URL=https://example.com/api/auth/github/callback
```

正式部署前还需要配置 Nginx 和 HTTPS，否则 GitHub OAuth 在线环境会不稳定，也不安全。
