# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、PostgreSQL 数据持久化、文章管理后台、邮箱登录鉴权、GitHub OAuth 登录、Docker Compose 一键启动、GitHub Actions 自动测试和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 1. 立即要做的事情

### 你需要做

1. 打开 GitHub 仓库的 `Actions` 页面。
2. 查看 `CI` 工作流是否在最新 push 后自动运行。
3. 确认三个 job 是否通过：
   - `Backend`
   - `Frontend`
   - `Compose`
4. 如果准备部署上线，提供云服务器信息：
   - 公网 IP
   - SSH 用户名
   - 部署目录
   - 域名，如果已有

### 我可以辅助完成

1. 排查 GitHub Actions 失败原因。
2. 增加更完整的后端测试。
3. 准备云服务器部署脚本。
4. 配置线上 Docker Compose、Nginx、域名和 HTTPS。
5. 把 GitHub Actions 扩展为自动部署。

## 2. 已完成版本：v0.8.0 GitHub Actions 自动测试

v0.8.0 已完成：

- 新增 `.github/workflows/ci.yml`。
- push 到 `main` 时自动运行 CI。
- PR 到 `main` 时自动运行 CI。
- 支持手动触发 `workflow_dispatch`。
- `Backend` job：安装 Python 3.12、安装后端依赖、编译后端代码、导入 FastAPI app。
- `Frontend` job：安装 Node 22、执行 `npm ci`、执行 `npm run build`。
- `Compose` job：检查 Docker Compose 版本并运行 `docker compose config`。
- README 已加入 GitHub Actions CI badge。

## 3. 推荐下一版本：v0.9.0 云服务器部署

### 你应该做

1. 准备一台云服务器。
2. 确认服务器系统，建议 Ubuntu 22.04 或 24.04。
3. 提供服务器公网 IP、SSH 用户名和部署目录。
4. 如果有域名，提供域名和 DNS 管理入口。

### 我可以辅助完成

1. 写服务器初始化脚本。
2. 安装 Docker 和 Docker Compose。
3. 配置线上 `.env`。
4. 配置线上 `docker compose up -d --build`。
5. 配置 Nginx 反向代理。
6. 配置 HTTPS 证书。
7. 后续把 GitHub Actions 扩展为自动部署。

## 4. 后续路线

建议按这个顺序继续：

1. v0.9.0：云服务器部署、Nginx、域名和 HTTPS。
2. v1.0.0：AI 每日技术新闻和文章 AI 总结。
3. v1.1.0：评论审核、小游戏排行榜、访问统计和管理后台增强。
4. v1.2.0：GitHub Actions 自动部署。

## 5. 现在的执行建议

建议你先打开 GitHub 仓库的 Actions 页面确认 CI 是否通过。CI 通过后，下一步就可以进入云服务器部署准备。
