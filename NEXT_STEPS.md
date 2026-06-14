# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、PostgreSQL 数据持久化、文章管理后台、邮箱登录鉴权、GitHub OAuth 登录和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 1. 立即要做的事情

### 你需要做

1. 在 GitHub 创建 OAuth App。
2. 本地开发时填写回调地址：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

3. 把 `Client ID`、`Client Secret` 和你的 GitHub 登录名填入环境变量：

```text
GITHUB_CLIENT_ID=你的 Client ID
GITHUB_CLIENT_SECRET=你的 Client Secret
GITHUB_ADMIN_LOGINS=你的 GitHub 登录名
```

4. 重启 FastAPI 后端。
5. 打开 `http://127.0.0.1:5173`，进入“登录”页，点击“使用 GitHub 登录”。

### 我可以辅助完成

1. 你提供 `Client ID` 和 `Client Secret` 后，我可以帮你写入本地 `.env` 或启动命令。
2. 验证 GitHub 登录回调是否成功。
3. 检查 GitHub 用户是否获得管理员权限。
4. 继续做 Docker Compose 一键启动。
5. 继续做 GitHub Actions、服务器部署、Nginx 和 HTTPS。

## 2. 已完成版本：v0.6.0 GitHub OAuth 登录

v0.6.0 已完成：

- 后端新增 GitHub OAuth 登录跳转接口：`GET /api/auth/github/start`。
- 后端新增 GitHub OAuth 回调接口：`GET /api/auth/github/callback`。
- OAuth state 使用 HMAC 签名并设置有效期。
- 后端通过 GitHub code 换取 access token，并读取 GitHub 用户资料和主邮箱。
- GitHub 用户会写入 `users.github_id`、`avatar_url` 和显示名称。
- 如果 GitHub 邮箱匹配已有账号，会自动绑定到该账号。
- `GITHUB_ADMIN_LOGINS` 或 `GITHUB_ADMIN_EMAILS` 匹配到的用户会获得管理员权限。
- 前端登录页新增“使用 GitHub 登录”按钮。
- 前端能识别 OAuth 回调带回的 token，并自动进入管理页。

## 3. 推荐下一版本：v0.7.0 Docker Compose 一键启动

### 你应该做

1. 确认 Docker Desktop 能稳定运行。
2. 确认希望本地统一访问入口，例如 `http://127.0.0.1:8080`。

### 我可以辅助完成

1. 给前端和后端分别写 Dockerfile。
2. 更新 `docker-compose.yml`，同时启动 frontend、backend、postgres。
3. 增加后端健康检查和前端代理配置。
4. 写清楚一键启动、停止、查看日志和清库命令。

## 4. 后续路线

建议按这个顺序继续：

1. v0.7.0：Docker Compose 一键启动。
2. v0.8.0：GitHub Actions 自动构建和测试。
3. v0.9.0：云服务器部署、Nginx、域名和 HTTPS。
4. v1.0.0：AI 每日技术新闻和文章 AI 总结。
5. v1.1.0：评论审核、小游戏排行榜、访问统计和管理后台增强。

## 5. 现在的执行建议

建议你先完成 GitHub OAuth App 配置。拿到 `Client ID` 和 `Client Secret` 后，我可以继续帮你做完整联调；联调通过后，再进入 Docker Compose 一键启动。
