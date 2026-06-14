# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、小游戏 iframe 响应式修正、PostgreSQL 数据持久化、文章管理后台、基础邮箱登录鉴权和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 1. 立即要做的事情

### 你需要做

1. 保持 Docker Desktop 和 Clash 运行。
2. 打开本地博客：`http://127.0.0.1:5173`。
3. 进入“登录”页；如果是新数据库，先选择“初始化管理员”，之后用同一邮箱密码登录。
4. 登录后进入“管理”页，检查文章发布、编辑、删除是否符合你的使用习惯。
5. 决定下一阶段优先方向：GitHub OAuth、完整 Docker Compose 一键启动，还是部署到云服务器。

### 我可以辅助完成

1. 继续使用 Clash 代理执行 `git push`。
2. 调整登录页和管理后台交互细节。
3. 接入 GitHub OAuth 登录。
4. 把前端、后端、数据库合并进完整 Docker Compose。
5. 配置 GitHub Actions、服务器部署、Nginx 和 HTTPS。

## 2. 已完成版本：v0.5.0 登录鉴权

v0.5.0 已完成：

- 后端新增 PBKDF2 密码哈希。
- 后端新增 HS256 token 鉴权。
- 新增接口：`POST /api/auth/register`、`POST /api/auth/login`、`GET /api/auth/me`。
- `POST/PUT/DELETE /api/admin/articles` 已要求管理员 token。
- 前端新增“登录”页，支持初始化管理员和登录。
- 前端管理页已加登录保护，未登录时不会显示后台表单。
- 登录状态保存到浏览器本地，刷新后通过 `/api/auth/me` 校验。
- 本地数据库启动时会自动给旧版 `users` 表补 `password_hash` 字段。
- 小游戏仓库修复了“局内打开规则页后返回开始页”的问题。

## 3. 推荐下一版本：v0.6.0 GitHub OAuth 登录

### 你应该做

1. 在 GitHub 创建 OAuth App。
2. 提供 GitHub OAuth App 的 `Client ID` 和 `Client Secret`。
3. 确认回调地址，本地开发建议先用：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

### 我可以辅助完成

1. 新增 GitHub OAuth 登录跳转和回调接口。
2. 把 GitHub 用户写入 `users.github_id`、`avatar_url`。
3. 管理员邮箱和 GitHub 账号绑定。
4. 前端登录页增加 GitHub 登录按钮。
5. 更新 `.env.example`、README、版本日志和验证步骤。

## 4. 另一个可选下一版本：v0.6.0 Docker Compose 一键启动

如果你想先把本地开发体验做稳，也可以先做 Docker Compose 一键启动。

### 你应该做

1. 确认 Docker Desktop 能稳定启动。
2. 确认是否希望本地访问统一入口，例如 `http://127.0.0.1:8080`。

### 我可以辅助完成

1. 给前端和后端分别写 Dockerfile。
2. 更新 `docker-compose.yml`，同时启动 frontend、backend、postgres。
3. 增加后端健康检查和前端代理配置。
4. 写清楚一键启动、停止、查看日志和清库命令。

## 5. 后续路线

建议按这个顺序继续：

1. v0.6.0：GitHub OAuth 登录，或 Docker Compose 一键启动。
2. v0.7.0：GitHub Actions 自动构建和测试。
3. v0.8.0：云服务器部署、Nginx、域名和 HTTPS。
4. v0.9.0：AI 每日技术新闻和文章 AI 总结。
5. v1.0.0：评论审核、小游戏排行榜、访问统计和管理后台增强。

## 6. 现在的执行建议

建议你先在本地完成一次完整验收：

1. 登录管理员账号。
2. 发布一篇测试文章。
3. 编辑这篇文章。
4. 删除这篇文章。
5. 打开小游戏，从局内进入规则页再返回，确认能回到局内。

验收通过后，下一步优先做 GitHub OAuth；如果你更想先部署上线，则先做 Docker Compose 一键启动和服务器部署。
