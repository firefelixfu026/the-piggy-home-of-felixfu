# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、PostgreSQL 数据持久化、文章管理后台、邮箱登录鉴权、GitHub OAuth 登录、Docker Compose 一键启动和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 1. 立即要做的事情

### 你需要做

1. 打开 Docker Desktop。
2. 在项目根目录执行：

```powershell
docker compose up -d --build
```

3. 打开 Docker 版博客：

```text
http://127.0.0.1:8080
```

4. 进入“登录”页，测试 GitHub 登录或邮箱登录。
5. 登录后进入“管理”页，测试文章发布、编辑、删除。

### 我可以辅助完成

1. 继续优化 Docker Compose 启动体验。
2. 配置 GitHub Actions 自动构建和测试。
3. 增加后端单元测试和前端构建检查。
4. 准备云服务器部署脚本。
5. 配置 Nginx、域名和 HTTPS。

## 2. 已完成版本：v0.7.0 Docker Compose 一键启动

v0.7.0 已完成：

- 新增 `backend/Dockerfile`。
- 新增 `frontend/Dockerfile`。
- 新增 `frontend/nginx.conf`，由 Nginx 服务静态前端并反向代理 `/api`。
- `docker-compose.yml` 已包含 `postgres`、`backend`、`frontend` 三个服务。
- 后端容器通过 `postgres:5432` 连接数据库。
- 前端统一访问入口为 `http://127.0.0.1:8080`。
- 后端调试入口保留为 `http://127.0.0.1:8000`。
- 新增 `.dockerignore`、`backend/.dockerignore`、`frontend/.dockerignore`，减少构建上下文。
- 新增 `DOCKER_COMPOSE.md`，记录一键启动、停止、验证和代理排查方式。

## 3. 推荐下一版本：v0.8.0 GitHub Actions 自动测试

### 你应该做

1. 确认 GitHub 仓库 Actions 功能可用。
2. 决定是否每次 push 都自动运行前端构建和后端编译检查。

### 我可以辅助完成

1. 新增 `.github/workflows/ci.yml`。
2. CI 中运行后端 Python 编译检查。
3. CI 中安装前端依赖并运行 `npm run build`。
4. 后续加入 Docker 镜像构建检查。
5. 在 README 中增加 CI 状态说明。

## 4. 后续路线

建议按这个顺序继续：

1. v0.8.0：GitHub Actions 自动构建和测试。
2. v0.9.0：云服务器部署、Nginx、域名和 HTTPS。
3. v1.0.0：AI 每日技术新闻和文章 AI 总结。
4. v1.1.0：评论审核、小游戏排行榜、访问统计和管理后台增强。

## 5. 现在的执行建议

建议你先用 Docker 版入口完成一次验收：

1. 打开 `http://127.0.0.1:8080`。
2. 登录管理员账号。
3. 发布一篇测试文章。
4. 编辑这篇文章。
5. 删除这篇文章。

验收通过后，下一步做 GitHub Actions，让每次推送自动验证前端构建和后端代码。
