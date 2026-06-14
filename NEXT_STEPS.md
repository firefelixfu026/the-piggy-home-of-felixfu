# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入和基础文档；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。  
当前待处理问题：最近两次提交已在本地完成，但 Git for Windows 连接 `github.com:443` 超时，还没有成功推送到 GitHub。排查细节见 [GITHUB_PUSH_TROUBLESHOOTING.md](./GITHUB_PUSH_TROUBLESHOOTING.md)。

## 1. 立即要做的事情

### 你需要做

1. 确认当前电脑网络可以访问 GitHub。
2. 如果使用代理或校园网，告诉我代理类型和端口，让我配置 Git 后重试推送。
3. 打开本地博客检查小游戏页是否符合预期：`http://127.0.0.1:5173`。
4. 按 [DOCKER_DESKTOP_SETUP.md](./DOCKER_DESKTOP_SETUP.md) 安装 Docker Desktop，并把验证命令输出发给我。
5. 确认下一步是否优先做“数据库持久化”，也就是把文章、评论、点赞、收藏、点踩从静态数据变成真实数据库数据。

### 我可以辅助完成

1. 网络恢复后执行 `git push`，把本地未推送提交同步到 GitHub。
2. 检查 GitHub 仓库里的文件结构是否完整。
3. 继续实现 v0.3.0：PostgreSQL + SQLAlchemy + 数据库表结构 + 基础 CRUD 接口。
4. 更新版本日志和代码分析文档，保持答辩材料可用。
5. 如果你提供代理端口，我可以配置 Git 代理并重试推送。

## 2. 推荐下一版本：v0.3.0 数据持久化版本

下一步最建议做数据库持久化。原因是当前博客已经“看得见、能展示”，但文章、评论和互动都还只是静态数据或内存数据；只要服务重启，新增评论和互动就会丢失。接入数据库后，后续登录注册、管理后台、评论审核、点赞收藏统计、AI 总结缓存都会有稳定基础。

v0.3.0 推荐目标：

- 使用 PostgreSQL 作为正式数据库。
- 使用 SQLAlchemy 作为后端 ORM。
- 创建数据库表：用户、文章、评论、互动、标签。
- 把 `/api/articles` 从内存数据改成数据库读取。
- 增加文章详情接口、评论提交接口和互动提交接口的数据库写入。
- 增加初始化种子数据，让本地环境启动后自动有示例文章。
- 增加 `docker-compose.yml`，一键启动 PostgreSQL。
- 更新 README，写清楚数据库启动、迁移和本地验证方式。

## 3. v0.3.0 分工

### 你应该做

- 按 `DOCKER_DESKTOP_SETUP.md` 安装并启动 Docker Desktop。
- 决定本地数据库账号密码是否使用默认开发配置。
- 确认示例文章内容是否先继续使用当前 3 篇占位文章。

### 我可以辅助完成

- 编写 `docker-compose.yml`。
- 编写 `.env.example` 中的数据库配置。
- 添加 SQLAlchemy 依赖。
- 编写数据库连接、模型和初始化脚本。
- 改造 FastAPI 接口，让文章、评论和互动走数据库。
- 添加基础 API 验证命令。
- 更新 `CHANGELOG.md` 和 `CODE_ANALYSIS.md`。
- 提交代码并推送 GitHub。

## 4. v0.3.0 后的下一步

数据库持久化完成后，建议按这个顺序继续：

1. v0.4.0：文章管理后台，支持管理员发布、编辑、删除文章。
2. v0.5.0：邮箱注册登录和基础 JWT 鉴权。
3. v0.6.0：GitHub OAuth 登录。
4. v0.7.0：Docker Compose 一键启动前端、后端、数据库。
5. v0.8.0：GitHub Actions 自动构建和测试。
6. v0.9.0：云服务器部署、Nginx、域名和 HTTPS。
7. v1.0.0：AI 每日技术新闻和文章 AI 总结。

## 5. 现在的执行建议

建议你先完成两件事：

1. 告诉我你是否有本地代理，以及代理端口是多少；或者使用 GitHub Desktop 先推送。
2. 安装 Docker Desktop，并把 `docker --version`、`docker compose version`、`wsl --list --verbose` 的输出发给我。

如果这两点都满足，就可以直接开始 v0.3.0 数据持久化开发。
