# 下一步开发计划

当前项目状态：已经完成本地 MVP、FastAPI 接口骨架、小游戏嵌入、PostgreSQL 数据持久化、文章管理后台、邮箱登录鉴权、GitHub OAuth 登录、Docker Compose 一键启动、GitHub Actions 自动测试和阶段性文档整理；本地 Git 仓库已绑定 GitHub 远程仓库 `https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git`。

当前最新阶段：v1.5.7 文章图片资源本地化修复。旧笔记 `Git` 中失效的飞书临时图片链接已替换为本站本地 Git 工作流示意图，后端启动时会自动修复数据库里已存在文章的旧链接。

GitHub 推送问题已通过 Clash `127.0.0.1:7897` 代理解决，排查细节已归档到 `docs/archive/GITHUB_PUSH_TROUBLESHOOTING.md`。

## 26. v1.5.7 已完成：文章图片资源本地化修复

本阶段已完成：

- 新增本站本地图片资源 `/articles/git-workflow.svg`，用于替换旧笔记中的 Git 结构图。
- 旧笔记源数据中的飞书临时下载链接已替换为本地图片地址。
- 后端种子逻辑会自动修复数据库里已存在的旧文章内容，把过期飞书链接替换为本地图片。
- 前端图片加载失败时会显示清楚的失败提示，不再只有浏览器默认破图图标。

部署后请重点测试：

1. 打开旧笔记 `Git`，滚动到 `Git 结构`。
2. 确认图片显示为 Git 工作区、暂存区、本地仓库、远程仓库示意图。
3. 如果线上刚部署完仍看到旧破图，等待容器重启完成后强制刷新浏览器缓存。
4. 检查文章其他 Markdown 格式没有回退。

下一阶段建议：继续做文章封面图和后台图片上传，把之后的文章图片都变成站内可控资源。

## 25. v1.5.6 已完成：Markdown 格式兼容增强

本阶段已完成：

- 支持 `#` 到 `######` 六级标题，修复旧笔记中 `####` 被当成普通文本的问题。
- 支持 Markdown 分隔线 `---`、`***`、`___`。
- 支持连续编号列表，思考题和作业题不再挤成一个段落。
- 支持基础 Markdown 表格，表格过宽时可横向滚动。
- 图片地址解析更宽容，减少外链图片因为地址较长或带标题而无法识别的问题。

部署后请重点测试：

1. 打开旧笔记 `Git`，确认“版本控制系统”“分支模型”等四级标题能正常变成小标题。
2. 检查 Git 文章里的图片位置，不应再显示整段 `![](...)` 原始文本。
3. 滚动到“思考题&作业题”，确认编号列表和表格比之前更清晰。
4. 用手机打开同一篇文章，确认宽表格可以横向滚动而不是撑破页面。

下一阶段建议：继续做文章资源本地化和封面图，把重要外链图片逐步保存到本站资源，降低 Feishu 等外链过期风险。

## 24. v1.5.5 已完成：Markdown 图片阅读体验

本阶段已完成：

- 文章正文支持独立 Markdown 图片语法 `![说明](图片地址)`。
- 文章正文支持段落里的行内图片语法。
- 图片默认懒加载，减少打开长文时的一次性加载压力。
- 图片增加最大宽度、圆角、边框和居中样式，避免长链接图片撑开正文区域。
- 行内图片限制最大宽度和高度，防止打乱段落排版。

部署后请重点测试：

1. 打开旧笔记里的 `Git` 文章，确认顶部外链图片位置不再显示为纯文本。
2. 在电脑浏览器缩窄窗口，确认图片不会横向撑破页面。
3. 用手机打开长篇笔记，确认图片、代码块和公式都能横向或自适应查看。
4. 在管理后台文章预览里输入一行 `![测试图片](https://example.com/test.png)`，确认会显示为图片块；如果图片地址无效，浏览器会显示破图占位，这是正常的网络资源状态。

下一阶段建议：继续做文章封面和内容资源本地化，把重要外链图片逐步迁移到站点可控资源里。

## 23. v1.5.4 已完成：旧版笔记迁移

本阶段已完成：

- 从旧版 GitHub Pages 笔记站 `https://firefelixfu026.github.io/FelixFu-no-website/` 迁移 6 篇文章。
- 已导入文章：Git、Vibe Coding、计算机网络、后端技术指南、前端三件套、React 基础与进阶。
- 新增统一标签 `旧笔记`，同时保留 Git、AI、计算机网络、后端、前端、React 等主题标签，方便文章页筛选。
- 后端启动时会自动补齐缺失的旧笔记文章；如果数据库里已经有同 ID 文章，则保持现有内容不变。
- 这次迁移不会清空评论、点赞、收藏、点踩、阅读次数或管理员账号。

部署后请重点测试：

1. 打开文章页，确认能看到 6 篇旧笔记。
2. 点击 `旧笔记` 标签，确认能筛选出迁移文章。
3. 打开长篇笔记，检查目录、代码块、表格、Markdown 和 LaTeX 显示是否正常。
4. 检查文章详情不再白屏，手机端也能打开正文。

下一阶段建议：继续完善文章内容体验，包括图片显示、长文阅读排版、文章封面和内容资源本地化。

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

## 19. GitHub Actions 自动部署已补充

已完成：

- 新增 `.github/workflows/deploy.yml`。
- 新增 `scripts/deploy-production.sh`。
- 新增 `GITHUB_ACTIONS_DEPLOYMENT.md`。

还需要在 GitHub 仓库配置 Secrets：

```text
DEPLOY_HOST=47.242.176.227
DEPLOY_USER=admin
DEPLOY_PORT=22
DEPLOY_PATH=/opt/felixfu-blog
DEPLOY_SSH_KEY=部署私钥内容
```

配置完成后，到 GitHub Actions 页面手动运行一次 `Deploy` workflow。成功后，后续每次 push 到 `main`，CI 通过后会自动部署到服务器。

下一步建议：

1. 生成部署 SSH key。
2. 把 public key 加到服务器 `~/.ssh/authorized_keys`。
3. 把 private key 加到 GitHub Secrets。
4. 手动触发一次 Deploy workflow 验证。
5. 验证成功后进入 v1.2.0：增强测试覆盖和内容功能。
## 20. GitHub Actions 自动部署首次运行修复

本次失败现象：

```text
Deploy on server 失败
chmod: cannot access 'scripts/deploy-production.sh': No such file or directory
```

判断结果：

```text
Validate deployment secrets 已通过
Configure SSH 已通过
说明 GitHub Secrets 和 SSH key 配置正确
失败原因是服务器目录还没拉取到最新的部署脚本
```

已修复：

```text
.github/workflows/deploy.yml 现在会先执行 git pull --ff-only
然后再 chmod +x scripts/deploy-production.sh
最后运行部署脚本
```

下一步：

1. 推送本次修复到 GitHub。
2. 回到 GitHub Actions 的 Deploy 页面重新运行 workflow。
3. 如果通过，自动部署链路即完成：push main -> CI -> Deploy -> 服务器更新。
## 21. 个人头像上线和自动部署验证

已完成：

```text
frontend/public/avatar.jpg 已加入项目
左侧栏品牌头像已替换为真实头像
首页个人展示图已替换为真实头像
npm run build 已通过
```

本次提交目的：

```text
验证 push 到 main 后，GitHub Actions 是否自动执行 CI，并在 CI 成功后自动 Deploy 到服务器。
```

上线后检查：

1. 打开 `https://www.felixfu.xyz`。
2. 刷新页面，必要时强制刷新浏览器缓存。
3. 检查左侧栏头像和首页个人图片是否已经变为真实头像。
4. 在 GitHub Actions 中确认最新一次 `CI` 和 `Deploy` 都是绿色通过。
## 22. 管理后台评论管理已完成

已完成：

```text
GET /api/admin/comments
DELETE /api/admin/comments/{comment_id}
管理后台新增评论管理区域
管理员可查看、刷新、删除全站评论
```

验证：

```text
python -m compileall backend\app 已通过
npm run build 已通过
```

上线后检查：

1. 打开 `https://www.felixfu.xyz` 并登录管理员账号。
2. 进入“文章”页发布一条测试评论。
3. 进入“管理”页查看“评论管理”区域是否出现新评论。
4. 点击删除，确认评论从文章页和后台列表中消失。

下一步建议：

1. 增加后端自动化测试，覆盖文章、评论、鉴权和管理接口。
2. 给管理后台增加访问统计或站点仪表盘。
3. 继续推进 AI 每日技术新闻和文章总结模块。
## 23. 管理员初始化安全加固已完成

问题：

```text
如果公开站点使用全新数据库，任何访客都有机会进入“登录”页抢先初始化管理员。
```

已修复：

```text
后端新增 ADMIN_SETUP_TOKEN 校验
未配置 ADMIN_SETUP_TOKEN 时默认拒绝初始化管理员
前端初始化管理员表单新增“初始化密钥”输入框
.env.example 和部署文档已补充该环境变量
```

当前影响：

```text
已有管理员登录不受影响
GitHub OAuth 管理员登录不受影响
以后如果重建数据库，需要先在服务器 .env 中设置 ADMIN_SETUP_TOKEN，再初始化管理员
```

上线后建议：

1. 等 GitHub Actions 自动部署完成。
2. 确认原有管理员仍可通过 GitHub 或邮箱登录。
3. 不要把 `ADMIN_SETUP_TOKEN` 发给任何访客，也不要提交到 GitHub。
## 24. 游客隐藏管理入口已完成

问题：

```text
游客进入网站时左侧导航仍能看到“管理”，点击后会进入管理员登录页面。
```

已修复：

```text
游客导航不再显示“管理”
管理员登录后才显示“管理”入口
未登录或非管理员状态进入后台视图时自动回到首页
```

上线后检查：

1. 退出登录后刷新网站，确认左侧没有“管理”。
2. 点击“登录”完成管理员登录。
3. 登录成功后确认左侧出现“管理”。
4. 点击“退出”后确认“管理”再次消失。
## 10. v1.2.3 已完成：账号级互动和评论分页

已完成：

- 清空旧的匿名点赞、收藏和点踩计数，之后以账号互动记录为准。
- 新增账号级互动记录，游客不能直接点赞、收藏、点踩或点击“？”。
- 同一账号对同一篇文章的同一种互动只能记录一次，刷新页面不会重复累计。
- 文章页新增“？”互动按钮。
- 评论输入限制为 300 字。
- 评论列表按显示长度分页，每页最多约 5 条短评论的展示量；长评论会占用更多分页额度。

下一阶段建议：

1. 增加文章详情页或展开/收起长文阅读体验。
2. 增加访客评论的昵称输入、评论审核状态和管理端批量处理。
3. 完成 ICP 备案后恢复微信、国内手机浏览器的正常直达访问。
## 11. v1.2.4 已完成：评论权限和长文本限宽修复

已完成：

- 游客不能再直接发表评论，评论接口需要登录 token。
- 评论作者名由后端从登录账号读取，GitHub 登录后不再统一显示为“访客”。
- 未登录点击点赞、收藏、点踩、“？”或发布评论时，只显示站内提示，不直接跳转登录页。
- 评论内容区域增加强制断行，连续数字、连续英文和长链接不会再撑破文章卡片。
- 评论输入区保持在文章卡片宽度内。
- 后台评论管理中的长评论也会自动换行。

下一阶段建议：继续优化文章详情阅读体验、评论昵称/审核流程和移动端细节。
## 12. v1.2.5 已完成：后台评论管理分页和限宽

已完成：

- 后台评论管理区改为分页展示，避免评论多时页面过长。
- 后台评论管理使用固定每页 5 条的分页规则；长评论只负责自动换行，不再影响后台分页数量。
- 后台评论文本、文章标题和管理行都增加强制断行与限宽，长数字或长链接不会撑破管理页面。

下一阶段建议：继续完善评论审核状态、批量删除和按文章筛选评论。
## 13. v1.2.6 已完成：评论体验修补

已完成：

- 评论管理新增按文章筛选。
- 评论管理新增按作者筛选。
- 删除评论后保留当前分页位置。
- 前台评论发布成功后显示“评论发布成功”。
- 评论发布失败时显示明确失败原因。
- 评论输入区显示当前登录账号身份，避免不知道会以谁的名字评论。

下一阶段建议：进入 v1.3.0 文章阅读体验版，新增文章详情页、Markdown 渲染和代码块样式。
## 14. v1.3.0 已完成：文章详情页和基础 Markdown 阅读

已完成：

- 文章页从“所有正文直接堆在列表里”调整为“摘要列表 + 详情页阅读”。
- 每篇文章新增“阅读全文”入口，进入详情后可以查看完整正文、互动按钮和评论区。
- 详情页新增返回文章列表按钮，避免阅读完后需要依赖浏览器返回。
- 正文新增基础 Markdown 渲染，支持标题、段落、列表、引用、代码块、行内代码、粗体、斜体、行内公式和公式块的展示。
- 已执行 `npm run build` 验证前端构建通过。

下一阶段建议：

1. 完善文章管理端预览，让发布前可以检查 Markdown 效果。
2. 增加文章归档和按月份/标签浏览。
3. 优化移动端文章详情页排版。
4. 后续如需更标准的数学公式渲染，再接入 KaTeX 或 MathJax。

## 15. v1.3.1 已完成：LaTeX 公式渲染和文章预览

已完成：

- 文章详情页接入 KaTeX，LaTeX 公式不再只是文本样式，而是渲染为数学排版。
- 支持行内公式：`$...$` 和 `\(...\)`。
- 支持块级公式：`$$...$$` 和 `\[...\]`，包括多行公式块。
- 公式渲染失败时保留原文兜底，避免单个公式写错导致整篇文章无法显示。
- 管理后台新增正文实时预览区，写文章时可提前检查 Markdown、代码块和公式效果。
- 已执行 `npm run build` 验证前端构建通过。

下一阶段建议：

1. 增加文章归档和按月份浏览。
2. 增加文章详情页目录或标题锚点。
3. 继续优化移动端文章阅读体验。
## 16. v1.4.0 已完成：文章月份归档和组合筛选

已完成：

- 文章页新增月份归档入口。
- 月份入口按文章日期自动生成，并显示对应文章数量。
- 搜索、标签和月份可以组合筛选。
- 没有匹配文章时显示空状态。
- 已执行 `npm run build` 验证前端构建通过。

## 17. v1.4.1 已完成：文章详情目录和标题锚点

已完成：

- 根据 Markdown 标题自动生成文章目录。
- 正文标题自动获得锚点。
- 点击目录项可以跳转到对应标题位置。
- 目录支持多级缩进，适合长文阅读。
- 已执行 `npm run build` 验证前端构建通过。

## 18. v1.4.2 已完成：移动端文章阅读体验优化

已完成：

- 手机端文章列表稳定单列显示。
- 手机端标签和月份归档支持横向滚动。
- 文章详情页标题、目录、正文、公式块留白更适合窄屏。
- 互动按钮在手机端改为两列布局。
- 返回、阅读全文和评论输入在手机端更容易点击。
- 已执行 `npm run build` 验证前端构建通过。

下一阶段建议：

1. 做文章管理端的草稿/发布状态。
2. 做评论审核状态，避免公开站点被随意刷评论。
3. 做访问统计和热门文章排行。
4. 做 AI 每日技术新闻摘要模块。

## 19. v1.5.0 已完成：文章草稿和发布状态

已完成：

- 后端 `articles` 表新增 `status` 字段，老文章默认保持已发布。
- 管理员发布或编辑文章时可以选择“已发布”或“草稿”。
- 公开文章列表和文章详情只展示已发布文章。
- 草稿文章的评论和互动接口也会对游客隐藏，避免通过接口直接访问草稿内容。
- 管理员登录后仍可以在管理后台查看、编辑和切换全部文章状态。
- 管理后台文章列表新增状态徽章，便于区分草稿和已发布文章。
- 已执行 `python -m compileall backend\app` 和 `npm run build` 验证通过。

下一阶段建议：

1. 做评论审核状态，避免公开站点被随意刷评论。
2. 做访问统计和热门文章排行。
3. 做 AI 每日技术新闻摘要模块。
4. 做内容图片上传和文章封面图。

## 20. v1.5.1 已完成：评论审核流程

已完成：

- 后端 `comments` 表新增 `status` 字段。
- 历史评论默认迁移为“已通过”，避免升级后原有评论突然消失。
- 新发布评论默认进入“待审核”，不会立刻出现在公开文章详情里。
- 公开文章详情只显示已通过评论；管理员登录后仍能在后台查看全部评论。
- 管理后台评论列表新增状态筛选，支持全部、待审核、已通过。
- 管理后台评论卡片新增状态徽章和“通过”按钮，保留原有删除能力。
- 评论发布成功后提示“审核通过后会公开显示”。
- 已执行 `python -m compileall backend\app` 和 `npm run build` 验证通过。

下一阶段建议：

1. 做访问统计和热门文章排行。
2. 做内容图片上传和文章封面图。
3. 做 AI 每日技术新闻摘要模块。
4. 补充更完整的后端自动化测试，覆盖文章状态、评论审核和权限边界。

## 21. v1.5.2 已完成：阅读次数和热门文章排行

已完成：

- 后端 `articles` 表新增 `view_count` 字段。
- 历史文章默认从 0 次阅读开始统计。
- 游客或普通用户打开文章详情时会自动增加一次阅读次数。
- 管理员查看文章详情不计入阅读次数，避免后台维护时刷高数据。
- 文章列表和文章详情顶部新增阅读次数显示。
- 文章中心新增“热门文章”模块，按阅读次数展示前 5 篇文章。
- 点击热门文章条目可直接进入对应文章详情。
- 已执行 `python -m compileall backend\app` 和 `npm run build` 验证通过。

下一阶段建议：

1. 做内容图片上传和文章封面图。
2. 做 AI 每日技术新闻摘要模块。
3. 增加更细的访问统计，例如今日阅读、总访问量和来源设备。
4. 补充后端自动化测试，覆盖文章状态、评论审核、阅读计数和权限边界。

## 22. v1.5.3 已完成：文章页白屏热修复

已完成：

- 修复进入文章页时组件漏传 `archiveOptions`、`selectedArchive` 和 `setSelectedArchive` 导致页面空白的问题。
- 文章页组件新增安全默认值，即使以后某个筛选参数漏传，也会尽量保持页面可渲染。
- 已执行 `npm run build` 验证前端构建通过。

下一阶段建议：

1. 先在线上验证文章页、文章详情、阅读次数和热门文章排行是否恢复正常。
2. 做内容图片上传和文章封面图。
3. 做 AI 每日技术新闻摘要模块。
4. 增加更细的访问统计，例如今日阅读、总访问量和来源设备。
