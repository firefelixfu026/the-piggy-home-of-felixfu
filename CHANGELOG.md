# 版本日志

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
