# 版本日志

## v1.1.0 - GitHub Actions 自动部署

- 新增 `.github/workflows/deploy.yml`，在 CI 成功后自动 SSH 到阿里云服务器执行部署。
- 新增 `scripts/deploy-production.sh`，统一服务器手动部署和 Actions 自动部署流程。
- 新增 `GITHUB_ACTIONS_DEPLOYMENT.md`，记录 SSH key、GitHub Secrets、手动触发和故障回退说明。
- 更新 `README.md` 和 `NEXT_STEPS.md`，补充自动部署入口和下一步配置清单。
## v1.0.2 - 备份验证和端口安全收紧

- 线上数据库备份已验证成功，生成 `felix_blog_20260704_023709.sql.gz`。
- HTTPS 证书自动续期 dry-run 已验证成功。
- `docker compose ps` 显示 backend、frontend、postgres 均正常运行。
- `docker-compose.yml` 的 `5432`、`8000`、`8080` 改为只绑定 `127.0.0.1`，避免公网绕过 Nginx 直连数据库、后端或前端容器。
- 已执行 `docker compose config` 验证配置合法。
## v1.0.1 - 服务器日常运维文档

- 新增 `SERVER_OPERATIONS.md`，记录 SSH 登录、服务状态、日志、更新、重启、Nginx、HTTPS、备份、磁盘检查和常见故障排查。
- 更新 `README.md`，增加上线后运维入口。
- 更新 `NEXT_STEPS.md`，把后续重点推进到备份验证、运维检查和自动部署。
## v1.0.0 - 数据库备份和恢复

- 新增 `DATABASE_BACKUP.md`，记录线上 PostgreSQL 手动备份、恢复、下载备份和自动备份流程。
- 新增 `scripts/backup-postgres.sh`，用于服务器上生成压缩数据库备份并清理旧备份。
- 新增 `scripts/restore-postgres.sh`，用于从 `.sql.gz` 备份恢复数据库，并在恢复前自动做安全备份。
- 更新 `.gitignore`，忽略本地生成的文档和代码备份目录。
## v0.9.4 - 文章正文展示修复

- 修复文章页只显示摘要、不显示正文的问题。
- 前端文章卡片新增正文区域，渲染 `article.content`。
- 正文区域保留换行并兼容纯文本和 Markdown 原文展示。
- 已执行 `npm run build` 验证前端构建通过。
## v0.9.3 - 正式域名 HTTPS 和 GitHub 登录成功

- 正式站点 `https://www.felixfu.xyz` 已可访问。
- HTTPS 已配置完成。
- GitHub OAuth 登录已验证成功。
- v0.9.0 云服务器部署目标基本完成，下一阶段进入上线后检查、内容发布、备份和自动化增强。
- 更新 `README.md`、`NEXT_STEPS.md`、`CLOUD_SERVER_DEPLOYMENT.md` 和 `GITHUB_OAUTH_APP_SETUP.md`。
## v0.9.2 - GitHub OAuth 环境变量排查

- 记录 GitHub 登录失败原因：服务器 `.env` 中 `GITHUB_CLIENT_ID` 未配置。
- 确认 GitHub OAuth App 的正式域名 URL 配置方向正确。
- 更新 `CLOUD_SERVER_DEPLOYMENT.md`、`NEXT_STEPS.md` 和 `GITHUB_OAUTH_APP_SETUP.md`，补充线上 `.env` 配置和重启命令。
## v0.9.1 - 域名解析正常，准备 HTTPS

- 记录域名 `www.felixfu.xyz` 的 A 记录已显示解析正常。
- 当前 HTTPS 仍未设置，下一步是在服务器配置 Nginx 正式域名和 Certbot 证书。
- 更新 `README.md`、`NEXT_STEPS.md`、`CLOUD_SERVER_DOMAIN_PREP.md` 和 `CLOUD_SERVER_DEPLOYMENT.md`，同步域名阶段状态。
## v0.9.0 - 阿里云公网 IP 部署成功

- 阿里云中国香港服务器公网 IP `47.242.176.227` 已可访问博客。
- Docker Compose 已在服务器启动前端、后端和 PostgreSQL。
- Nginx 已完成 80 端口反向代理到前端容器。
- 当前仍等待域名审批，后续需要配置 DNS、HTTPS 和 GitHub OAuth 正式回调。
- 更新 `README.md`、`NEXT_STEPS.md` 和 `CLOUD_SERVER_DEPLOYMENT.md`，记录公网 IP 阶段部署成功。
## v0.8.5 - Docker 环境验证通过

- 记录阿里云服务器已完成 Docker 安装。
- 记录版本：`Docker version 29.0.1`、`Docker Compose version v5.3.0`。
- 下一步调整为：拉取 GitHub 仓库、配置线上 `.env`、启动 Docker Compose，并配置 Nginx 反向代理到公网 IP。
## v0.8.4 - SSH 和防火墙状态确认

- 记录阿里云服务器 SSH 用户名为 `admin`。
- 记录服务器密码已设置，后续建议切换为 SSH 密钥。
- 记录阿里云轻量服务器防火墙已开放 `22`、`80`、`443`。
- 更新下一步为：在服务器中安装 Docker、拉取仓库并启动 Docker Compose。
## v0.8.3 - 阿里云服务器信息记录

- 记录已购买的阿里云中国香港服务器信息：Ubuntu 22.04、2 vCPU、2 GiB、40 GiB、公网 IP `47.242.176.227`。
- 更新 `CLOUD_SERVER_DEPLOYMENT.md`，明确域名审批前先使用公网 IP 部署和验证。
- 更新 `NEXT_STEPS.md`，把下一步调整为 SSH 连接服务器并部署 Docker Compose。
- 更新 `README.md` 和 `CLOUD_SERVER_DOMAIN_PREP.md`，同步当前服务器和域名审批状态。
## v0.8.2 - 阿里云部署路线确认

- 明确 v0.9.0 云部署优先使用阿里云。
- 更新 `CLOUD_SERVER_DOMAIN_PREP.md`，新增阿里云购买建议、地域选择、安全组端口和备案路线。
- 更新 `CLOUD_SERVER_DEPLOYMENT.md`，新增阿里云购买、控制台、安全组、DNS 配置说明。
- 更新 `NEXT_STEPS.md`，把下一阶段调整为 v0.9.0 阿里云服务器部署。
- 更新 `README.md`，在下一步中明确阿里云优先路线。
## v0.8.1 - 启动和云部署文档整理

- 新增 `CLOUD_SERVER_DEPLOYMENT.md`，记录从服务器初始化到 Docker Compose、Nginx、DNS、HTTPS 和 GitHub OAuth 上线配置的完整流程。
- 更新 `README.md`，补充本地 Docker Compose 快速启动入口和 v0.9.0 云部署路线。
- 更新 `NEXT_STEPS.md`，明确当前阶段是 v0.8.1 文档整理版，下一步是 v0.9.0 云服务器部署。
- 更新 `DOCKER_COMPOSE.md`，增加快速启动清单和云服务器部署关系说明。
- 更新 `CLOUD_SERVER_DOMAIN_PREP.md`，增加部署执行入口并链接到云部署指南。
## v0.8.0 - GitHub Actions 自动测试

- 新增 `.github/workflows/ci.yml`。
- 新增 `CLOUD_SERVER_DOMAIN_PREP.md`，记录云服务器、域名、备案、DNS 和 HTTPS 准备事项。
- CI 在 push 到 `main`、PR 到 `main`、手动触发时运行。
- 新增 `Backend` job：安装 Python 3.12、安装后端依赖、编译后端代码、导入 FastAPI app。
- 新增 `Frontend` job：安装 Node 22、执行 `npm ci`、执行 `npm run build`。
- 新增 `Compose` job：检查 Docker Compose 版本并执行 `docker compose config`。
- README 新增 CI badge。
- 更新 README、下一步计划、数据库说明、Docker Compose 文档和代码分析文档。

## v0.7.0 - Docker Compose 一键启动

- 新增 `backend/Dockerfile`，容器内运行 FastAPI 后端。
- 新增 `frontend/Dockerfile`，使用 Node 构建前端，再由 Nginx 服务静态文件。
- 新增 `frontend/nginx.conf`，把 `/api` 反向代理到后端容器。
- 扩展 `docker-compose.yml`，支持 `postgres`、`backend`、`frontend` 三服务一键启动。
- 新增 Docker 健康检查，后端依赖数据库健康后启动，前端依赖后端健康后启动。
- 新增 `.dockerignore`、`backend/.dockerignore`、`frontend/.dockerignore`，减少构建上下文。
- 新增 `DOCKER_COMPOSE.md`，记录启动、停止、验证、Clash 代理和 OAuth 配置方式。
- README 和下一步计划已更新为 Docker Compose 优先。

## v0.6.0 - GitHub OAuth 登录

- 新增 GitHub OAuth 登录跳转和回调接口。
- 新增 GitHub code 换取 access token、读取用户资料和主邮箱的后端模块。
- OAuth state 使用 HMAC 签名并设置有效期。
- GitHub 用户登录后会写入 `users.github_id`、`avatar_url` 和显示名称。
- 支持通过 GitHub 邮箱绑定已有账号。
- 支持 `GITHUB_ADMIN_LOGINS` 和 `GITHUB_ADMIN_EMAILS` 指定 GitHub 管理员。
- 前端登录页新增“使用 GitHub 登录”按钮。
- 前端支持解析 OAuth 回调 token，登录后自动进入管理页。
- 新增 `GITHUB_OAUTH_APP_SETUP.md`，记录 GitHub OAuth App 创建和本地环境变量配置步骤。
- 更新 README、数据库说明、下一步计划和代码分析文档。

## v0.5.0 - 登录鉴权和后台保护

- 新增后端鉴权工具：PBKDF2 密码哈希、HS256 token 签发和校验。
- 新增认证接口：初始化管理员、登录、获取当前用户。
- `POST/PUT/DELETE /api/admin/articles` 已要求管理员 Bearer token。
- 前端新增“登录”页，支持初始化管理员和邮箱密码登录。
- 前端管理页已加登录保护，未登录时显示登录表单。
- 登录状态保存到浏览器本地，刷新后通过 `/api/auth/me` 校验。
- 本地数据库启动时会自动给旧版 `users` 表补充 `password_hash` 字段。
- 修复小游戏仓库中局内打开规则页后返回开始页的问题，相关提交已推送到 `card-war-made-by-class-3`。

## v0.4.0 - 文章管理后台

- 新增后端管理接口：创建、编辑、删除文章。
- 新增前端“管理”页，支持填写标题、摘要、正文、标签、日期和阅读时长。
- 管理页可编辑已有文章、删除文章，并自动刷新文章列表。
- 整理 Markdown 文件，把阶段性安装/排查/旧流程文档移入 `docs/archive/`。
- 修复小游戏仓库中开始游戏后的界面滚动问题，相关提交已推送到 `card-war-made-by-class-3`。
- 更新 README、版本日志、代码分析文档和下一步计划。

## v0.3.0 - PostgreSQL 数据持久化版本

- 新增 `docker-compose.yml`，通过 Docker Compose 启动 PostgreSQL。
- 新增 SQLAlchemy 数据库层、数据模型和种子数据初始化。
- 后端 `/api/articles`、`/api/articles/{id}/comments`、`/api/articles/{id}/reaction` 改为数据库读写。
- 前端评论、点赞、收藏、点踩改为调用后端接口，数据可持久化。
- 新增 `DATABASE.md`，记录数据库启动、表结构、接口行为和验证命令。
- 更新 README、下一步计划和代码分析文档。

## v0.2.3 - Git 代理和小游戏响应式修正

- 为当前仓库配置 Git 本地代理 `http://127.0.0.1:7897`，通过 Clash 成功恢复 GitHub 推送。
- 将之前本地未推送的 3 个提交推送到 GitHub `main` 分支。
- 调整小游戏嵌入布局，从两列占位改为上方控制条 + 下方全宽 iframe，避免压缩游戏宽度。
- 更新 `GITHUB_PUSH_TROUBLESHOOTING.md` 和 `NEXT_STEPS.md`，记录 GitHub 推送问题已解决。

## v0.2.2 - Docker 与 GitHub 推送准备文档

- 新增 `DOCKER_DESKTOP_SETUP.md`，说明 Docker Desktop、WSL/Ubuntu、Docker Compose 的安装和验证步骤。
- 新增 `GITHUB_PUSH_TROUBLESHOOTING.md`，记录 GitHub 推送失败的排查结果和代理/GitHub Desktop/API 三种替代方案。
- 更新 `NEXT_STEPS.md` 和 README，把 Docker 安装与 GitHub 推送排查作为 v0.3.0 前置事项。

## v0.2.1 - 下一步计划文档

- 新增 `NEXT_STEPS.md`，明确当前状态、下一步推荐方向和 v0.3.0 数据持久化计划。
- 更新 README，修正 GitHub 远程仓库状态，并加入下一步开发入口。
- 更新代码分析文档，记录新增文档的用途。

## v0.2.0 - 小游戏嵌入版

- 将小游戏模块从占位入口改为直接嵌入 GitHub Pages 在线页面。
- 新增“刷新游戏”“新窗口打开”“查看仓库”三个操作入口。
- 后端 `/api/game/card-war` 接口新增 `playUrl`，返回小游戏在线访问地址。
- 更新代码分析文档，记录小游戏集成方式。

## v0.1.0 - 本地 MVP 起步版

- 重写 `需求.md`，将原始需求整理为系统化 PRD 和阶段计划。
- 创建 React 前端项目骨架。
- 创建 FastAPI 后端接口骨架。
- 实现个人主页、文章列表、搜索、互动按钮、AI 模块和小游戏入口的前端雏形。
- 增加 README 和代码分析文档。
- 暂未接入 PostgreSQL、GitHub OAuth、GitHub Actions 和云服务器部署。














