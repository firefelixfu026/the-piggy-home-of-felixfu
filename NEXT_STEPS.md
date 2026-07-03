# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、PostgreSQL 数据持久化、文章管理后台、邮箱登录鉴权、GitHub OAuth 登录、Docker Compose 一键启动、GitHub Actions 自动测试和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

当前最新阶段：v0.9.3 正式域名 HTTPS 和 GitHub OAuth 登录成功。项目已通过阿里云中国香港服务器上线，正式地址为 `https://www.felixfu.xyz`；下一步进入上线后检查、内容发布、备份和自动化增强。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 1. 现在应该怎么启动

推荐使用 Docker Compose 一键启动：

```powershell
cd E:\FelixFu\document\网站\FelixFu
docker compose up -d --build
```

访问：

```text
http://127.0.0.1:8080
```

检查后端：

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8080/api/health'
```

完整启动、停止和排查步骤见 [DOCKER_COMPOSE.md](./DOCKER_COMPOSE.md)。

## 2. 当前云平台选择：阿里云

当前决定：优先使用阿里云完成 v0.9.0 云服务器部署。

推荐第一阶段选择：

```text
阿里云中国香港轻量应用服务器或 ECS
Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
2 vCPU / 2 GB / 40 GB 起步
阿里云购买 .com 域名
暂不备案，先快速上线
```

如果后续确定主要面向中国大陆访问，再切换到阿里云大陆地域并走 ICP 备案。


## 3. 已购买服务器

当前阿里云服务器已经就绪：

```text
地域：中国香港
实例名称：Ubuntu-qfmm
公网 IP：47.242.176.227
系统：Ubuntu 22.04
规格：2 vCPU / 2 GiB / 40 GiB
到期时间：2026-08-03 23:59:59
```

域名已经购买，但还没审批通过。现在可以先用公网 IP 部署：

```text
http://47.242.176.227
```

域名审批通过后，再把域名解析到 `47.242.176.227`，并配置 HTTPS。

下一步需要你提供或确认：

```text
SSH 用户名：admin
SSH 登录方式：密码已设置
防火墙：22、80、443 已开放
Docker：Docker version 29.0.1
Docker Compose：Docker Compose version v5.3.0
```
## 4. 立即要做的事情

### 你需要做

1. 打开 GitHub 仓库的 `Actions` 页面。
2. 查看 `CI` 工作流是否在最新 push 后自动运行。
3. 确认三个 job 是否通过：
   - `Backend`
   - `Frontend`
   - `Compose`
4. 如果准备部署上线，准备云服务器信息：
   - 公网 IP
   - SSH 用户名
   - 部署目录，例如 `/opt/felixfu-blog`
   - 域名，如果已有
5. 购买前先阅读 [CLOUD_SERVER_DOMAIN_PREP.md](./CLOUD_SERVER_DOMAIN_PREP.md)。
6. 真正开始部署时按 [CLOUD_SERVER_DEPLOYMENT.md](./CLOUD_SERVER_DEPLOYMENT.md) 执行。

### 我可以辅助完成

1. 排查 GitHub Actions 失败原因。
2. 增加更完整的后端测试。
3. 准备或执行云服务器初始化步骤。
4. 配置线上 Docker Compose、Nginx、域名和 HTTPS。
5. 把 GitHub Actions 扩展为自动部署。

## 5. 已完成版本：v0.8.0 GitHub Actions 自动测试

v0.8.0 已完成：

- 新增 `.github/workflows/ci.yml`。
- push 到 `main` 时自动运行 CI。
- PR 到 `main` 时自动运行 CI。
- 支持手动触发 `workflow_dispatch`。
- `Backend` job：安装 Python 3.12、安装后端依赖、编译后端代码、导入 FastAPI app。
- `Frontend` job：安装 Node 22、执行 `npm ci`、执行 `npm run build`。
- `Compose` job：检查 Docker Compose 版本并运行 `docker compose config`。
- README 已加入 GitHub Actions CI badge。

## 6. 文档整理版：v0.8.1 启动和部署说明

v0.8.1 文档更新：

- README 增加快速启动和云部署入口。
- DOCKER_COMPOSE 增加本地启动清单和云部署关系说明。
- 新增 CLOUD_SERVER_DEPLOYMENT，记录云服务器部署步骤。
- CLOUD_SERVER_DOMAIN_PREP 增加部署执行入口。
- NEXT_STEPS 更新为 v0.9.0 云服务器部署前的行动清单。

## 7. 推荐下一版本：v0.9.0 阿里云服务器部署

### 你应该做

1. 准备一台云服务器。
2. 确认服务器系统，建议 Ubuntu 22.04 或 24.04。
3. 提供服务器公网 IP、SSH 用户名和部署目录。
4. 如果有域名，提供域名和 DNS 管理入口。
5. 正式上线前重新生成 GitHub OAuth Client Secret。

### 我可以辅助完成

1. 安装 Docker 和 Docker Compose。
2. 拉取 GitHub 仓库代码。
3. 配置线上 `.env`。
4. 执行 `docker compose up -d --build`。
5. 配置 Nginx 反向代理。
6. 配置 HTTPS 证书。
7. 验证 GitHub OAuth 和管理后台。

## 8. 后续路线

建议按这个顺序继续：

1. v0.9.0：云服务器部署、Nginx、域名和 HTTPS。
2. v1.0.0：AI 每日技术新闻和文章 AI 总结。
3. v1.1.0：评论审核、小游戏排行榜、访问统计和管理后台增强。
4. v1.2.0：GitHub Actions 自动部署。

## 9. 公网 IP 部署结果

```text
访问地址：http://47.242.176.227
状态：已可打开
服务器：阿里云中国香港 Ubuntu 22.04
当前阶段：公网 IP 部署成功，等待域名审批
```

现在可以先进入网站“登录”页面，初始化管理员账号。域名审批通过后，再完成：

1. 阿里云 DNS 解析到 `47.242.176.227`。
2. Nginx server_name 改成正式域名。
3. Certbot 配置 HTTPS。
4. GitHub OAuth App 回调地址改成正式域名。
5. 服务器 `.env` 中 `FRONTEND_ORIGIN` 和 `GITHUB_OAUTH_CALLBACK_URL` 改成正式域名。

## 10. 域名解析状态

```text
域名：www.felixfu.xyz
解析状态：正常
HTTPS：未设置
下一步：服务器切换正式域名并签发 HTTPS 证书
```

需要完成：

1. 服务器 `.env` 更新为 `https://www.felixfu.xyz`。
2. Nginx 配置 `server_name www.felixfu.xyz`。
3. Certbot 签发 HTTPS 证书。
4. GitHub OAuth App 更新正式回调地址。

## 11. GitHub OAuth 环境变量问题已解决

当前 GitHub OAuth App 页面中的正式域名配置已经正确：

```text
Homepage URL: https://www.felixfu.xyz
Authorization callback URL: https://www.felixfu.xyz/api/auth/github/callback
```

此前网站登录页曾显示：

```text
GITHUB_CLIENT_ID is not configured
```

该问题已经通过补充服务器 `/opt/felixfu-blog/.env` 中的 `GITHUB_CLIENT_ID`、`GITHUB_CLIENT_SECRET`、`GITHUB_OAUTH_CALLBACK_URL` 和 `GITHUB_ADMIN_LOGINS` 解决。GitHub OAuth 登录已验证成功。

## 12. v0.9.3 正式上线检查

当前状态：

```text
正式地址：https://www.felixfu.xyz
公网 IP：http://47.242.176.227
HTTPS：已成功
GitHub OAuth：已成功
部署阶段：v0.9.0 基本完成
```

下一步优先级：

1. 初始化或确认管理员账号。
2. 进入“管理”页面发布一篇正式文章或测试文章。
3. 测试文章评论、点赞、收藏、点踩。
4. 测试 Certbot 自动续期：`sudo certbot renew --dry-run`。
5. 给服务器配置基础备份策略。
6. 后续把 GitHub Actions 从 CI 扩展为自动部署。

## 13. 推荐下一版本：v1.0.0 内容和自动化增强

建议 v1.0.0 做这些事：

1. 发布第一批正式博客内容。
2. 增加数据库备份和恢复文档。
3. 增加服务器日常运维命令文档。
4. 增强后端测试覆盖。
5. 设计 AI 每日技术新闻和文章 AI 总结模块。
6. 准备 GitHub Actions 自动部署。

## 14. 现在的执行建议

建议先在本地执行一次：

```powershell
cd E:\FelixFu\document\网站\FelixFu
docker compose up -d --build
```

确认 `http://127.0.0.1:8080` 可以访问后，再进入云服务器采购和部署准备。










## 15. 文章正文展示修复

问题：

```text
用户在文章页只能看到标题、摘要、标签、互动和评论，看不到正文内容。
```

原因：

```text
前端 ArticleWorkspace 渲染文章卡片时只输出了 article.summary，没有输出 article.content。
```

修复：

```text
frontend/src/App.jsx 增加 article.content 正文区域。
frontend/src/styles.css 增加 .article-content 样式，保留换行并兼容 Markdown 原文展示。
```

验证：

```text
npm run build 已通过。
```

## 16. 数据库备份和恢复已补充

已完成：

- 新增 `DATABASE_BACKUP.md`。
- 新增 `scripts/backup-postgres.sh`。
- 新增 `scripts/restore-postgres.sh`。
- `.gitignore` 已忽略本地备份目录。

服务器下一步可执行：

```bash
cd /opt/felixfu-blog
git pull
chmod +x scripts/backup-postgres.sh scripts/restore-postgres.sh
./scripts/backup-postgres.sh
```

建议确认备份成功后，再配置每日自动备份 cron。

## 17. 服务器日常运维文档已补充

已完成：

- 新增 `SERVER_OPERATIONS.md`。
- README 已增加上线后运维入口。
- 运维文档覆盖服务状态、日志、更新、重启、Nginx、HTTPS、备份、磁盘和故障排查。

服务器建议立即执行：

```bash
cd /opt/felixfu-blog
git pull
chmod +x scripts/backup-postgres.sh scripts/restore-postgres.sh
./scripts/backup-postgres.sh
sudo certbot renew --dry-run
docker compose ps
```

如果以上都通过，下一阶段可以做 GitHub Actions 自动部署。

## 18. 备份、证书续期和端口安全已验证

已验证：

```text
数据库备份：felix_blog_20260704_023709.sql.gz 已生成
HTTPS 续期：sudo certbot renew --dry-run 成功
容器状态：backend、frontend、postgres 正常运行
```

安全收紧：

```text
127.0.0.1:5432:5432  PostgreSQL 只允许服务器本机访问
127.0.0.1:8000:8000  FastAPI 后端只允许服务器本机访问
127.0.0.1:8080:80    前端容器只允许服务器本机访问，由 Nginx 对外代理
```

下一步在服务器执行：

```bash
cd /opt/felixfu-blog
git pull
docker compose up -d --force-recreate postgres backend frontend
docker compose ps
curl -I https://www.felixfu.xyz
```

完成后继续推进 GitHub Actions 自动部署。
