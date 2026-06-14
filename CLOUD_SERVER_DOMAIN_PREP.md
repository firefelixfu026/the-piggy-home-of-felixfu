# 云服务器与域名购买准备指南

本文档用于准备把当前博客从本地 Docker Compose 部署到云服务器，并购买自有域名。

当前已有站点：

- 学习笔记站点：`https://firefelixfu026.github.io/FelixFu-no-website/`
- 当前博客仓库：`https://github.com/firefelixfu026/the-piggy-home-of-felixfu`

建议目标：

- 新博客部署到云服务器。
- 旧学习笔记站点先保留在 GitHub Pages。
- 后续用同一个域名管理多个入口，例如：

```text
www.example.com      -> 新个人博客，云服务器
api.example.com      -> 后端接口，可选
notes.example.com    -> 旧学习笔记，GitHub Pages
```

## 1. 先决定部署路线

### 路线 A：国内大陆服务器

适合：

- 主要访问者在中国大陆。
- 希望访问速度稳定。
- 接受 ICP 备案流程。

注意：

- 在中国大陆提供非经营性互联网信息服务通常需要 ICP 备案。
- 域名、服务器、备案主体信息需要一致或符合云厂商备案要求。
- 备案完成前，国内云厂商通常不会允许你用该域名正式对外提供网站服务。

### 路线 B：香港或海外服务器

适合：

- 想先尽快上线。
- 暂时不想走 ICP 备案。
- 可以接受大陆访问速度可能不如大陆服务器。

注意：

- 香港/海外服务器一般不走中国大陆 ICP 备案流程。
- 如果后续使用中国大陆 CDN、加速、对象存储绑定域名，仍可能被要求备案。
- 对大陆访问体验、稳定性和合规要求要单独评估。

### 本项目建议

如果你只是个人学习和展示，建议先选：

```text
香港或新加坡轻量云服务器 + .com 域名
```

这样能更快完成首次上线。等网站内容稳定后，再考虑大陆服务器和 ICP 备案。

如果你希望国内访问体验更好，建议选：

```text
阿里云/腾讯云大陆服务器 + 同平台购买域名 + ICP 备案
```

同平台购买服务器和域名，备案流程通常更顺。

## 2. 云服务器购买建议

可选云厂商：

- 腾讯云 CVM 或轻量应用服务器
- 阿里云 ECS 或轻量应用服务器
- 华为云 ECS

当前项目是 Docker Compose 三服务：

- frontend：Nginx 静态前端
- backend：FastAPI
- postgres：PostgreSQL

### 推荐配置

最低可用：

```text
CPU: 1 vCPU
内存: 2 GB
系统盘: 40 GB
带宽: 2-3 Mbps
系统: Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
```

更推荐：

```text
CPU: 2 vCPU
内存: 2-4 GB
系统盘: 40-80 GB
带宽: 3-5 Mbps
系统: Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
```

原因：

- Docker 构建前端时会占用一定内存。
- PostgreSQL、FastAPI、Nginx 同时运行，2 GB 内存更稳。
- 个人博客流量不大，3 Mbps 起步通常够用。

### 购买时建议填写

```text
地域:
国内路线选上海/杭州/广州/北京等离访问者近的区域；
快速上线路线选中国香港或新加坡。

镜像:
Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS

登录方式:
优先 SSH 密钥；
如果先用密码，后续部署时再改成 SSH 密钥。

公网 IP:
必须购买或分配。

安全组:
开放 22、80、443。
不要对公网开放 5432。
8000 后续只用于内网或本机调试，正式上线不应直接公网开放。
```

### 安全组规则

入站规则建议：

```text
TCP 22    SSH，建议只允许你的 IP
TCP 80    HTTP，允许 0.0.0.0/0
TCP 443   HTTPS，允许 0.0.0.0/0
```

不要开放：

```text
TCP 5432  PostgreSQL
TCP 8000  FastAPI 直连端口
```

后续线上结构应是：

```text
浏览器 -> HTTPS 443 -> Nginx -> Docker frontend/backend
```

## 3. 域名购买建议

### 域名后缀

优先推荐：

```text
.com
.net
.cn
```

建议：

- 如果想少折腾，先买 `.com`。
- 如果买 `.cn`，通常实名要求更严格，且国内访问/备案链路更紧。
- 域名尽量短、好记、不要包含太多连字符。

可考虑：

```text
felixfu.com
felixfu.cn
felixfu.blog
fujfan.com
```

实际是否可注册要以域名注册商查询结果为准。

### 购买平台

如果买国内大陆服务器：

```text
服务器在哪里买，域名也尽量在哪里买。
```

这样备案资料、域名实名认证、备案接入会更顺。

如果买香港/海外服务器：

```text
域名可以在阿里云、腾讯云、Cloudflare、Namecheap 等平台购买。
```

但为了你后续操作简单，国内账号已实名的话，阿里云或腾讯云更容易上手。

## 4. ICP 备案注意事项

如果服务器在中国大陆，并且使用自有域名对公网提供网站服务，需要准备 ICP 备案。

通常需要：

- 云账号实名认证。
- 域名实名认证。
- 一台符合备案要求的云服务器。
- 个人身份证信息。
- 网站名称、网站用途、负责人联系方式。
- 按云厂商流程进行真实性核验。

备案完成后：

- 网站底部需要展示备案号。
- 备案号需要链接到工信部备案系统。
- 部分场景还需要做公安联网备案。

如果服务器在香港/海外：

- 通常不走大陆 ICP 备案。
- 但如果未来接入大陆 CDN、国内对象存储、国内加速服务，可能仍需要备案。

## 5. DNS 规划

假设你买到域名：

```text
example.com
```

建议先这样规划：

```text
example.com          -> 新博客
www.example.com      -> 新博客
notes.example.com    -> 旧学习笔记站点
```

### 新博客 DNS

云服务器拿到公网 IP 后，添加 DNS：

```text
类型: A
主机记录: @
记录值: 云服务器公网 IP

类型: A
主机记录: www
记录值: 云服务器公网 IP
```

也可以：

```text
www CNAME example.com
```

### 旧学习笔记 DNS

旧学习笔记目前在 GitHub Pages：

```text
https://firefelixfu026.github.io/FelixFu-no-website/
```

如果要绑定到：

```text
notes.example.com
```

一般做法：

1. 在 DNS 中添加：

```text
类型: CNAME
主机记录: notes
记录值: firefelixfu026.github.io
```

2. 到 `FelixFu-no-website` 仓库的 GitHub Pages 设置里，配置 custom domain：

```text
notes.example.com
```

GitHub Pages 官方支持给 Pages 站点绑定自定义域名，并支持 apex domain 和 subdomain。

## 6. GitHub OAuth 上线后要改什么

当前本地 OAuth 回调是：

```text
http://127.0.0.1:8000/api/auth/github/callback
```

上线后需要改成你的正式域名，例如：

```text
https://www.example.com/api/auth/github/callback
```

GitHub OAuth App 里需要改：

```text
Homepage URL:
https://www.example.com

Authorization callback URL:
https://www.example.com/api/auth/github/callback
```

服务器 `.env` 也要改：

```text
FRONTEND_ORIGIN=https://www.example.com
GITHUB_OAUTH_CALLBACK_URL=https://www.example.com/api/auth/github/callback
GITHUB_ADMIN_LOGINS=你的 GitHub 登录名
```

注意：

- 你之前把 Client Secret 发到聊天里了。
- 正式上线前建议在 GitHub OAuth App 页面重新生成一个新的 Client Secret。
- 新 Secret 只放到服务器 `.env`，不要提交到 GitHub。

## 7. HTTPS 准备

上线后必须配置 HTTPS。

推荐方案：

```text
Nginx + Certbot + Let's Encrypt
```

准备条件：

- 域名已经解析到服务器公网 IP。
- 服务器安全组开放 80 和 443。
- Nginx 能通过 80 端口正常响应。
- 可以 SSH 登录服务器并使用 sudo。

Certbot 官方说明中也强调，常见 Nginx/HTTP 验证方式需要网站能通过 80 端口访问。

## 8. 你购买后需要提供给我什么

购买云服务器后，请提供：

```text
云厂商:
服务器地域:
服务器公网 IP:
操作系统:
SSH 用户名:
SSH 登录方式: 密钥 / 密码
部署目录:
```

购买域名后，请提供：

```text
域名:
DNS 管理平台:
是否已实名认证:
是否准备 ICP 备案:
```

如果已经完成备案，请提供：

```text
ICP备案号:
公安备案状态:
```

GitHub OAuth 正式上线前，请提供或确认：

```text
新的 GITHUB_CLIENT_ID:
新的 GITHUB_CLIENT_SECRET:
GitHub 登录名:
```

如果你不想直接把服务器密码发给我，也可以：

1. 你在本机执行我给你的命令。
2. 或者你创建一个临时 SSH 密钥。
3. 部署完成后删除临时密钥。

## 9. 推荐购买清单

快速上线版本：

```text
服务器: 腾讯云/阿里云 中国香港轻量应用服务器
系统: Ubuntu 22.04 LTS
配置: 2 vCPU / 2 GB / 40 GB
带宽: 3-5 Mbps
域名: .com
备案: 暂不备案
```

国内稳定访问版本：

```text
服务器: 腾讯云/阿里云 中国大陆 CVM/ECS
系统: Ubuntu 22.04 LTS
配置: 2 vCPU / 2-4 GB / 40-80 GB
带宽: 3-5 Mbps
域名: 同平台购买 .com 或 .cn
备案: ICP 备案
```

## 10. 参考资料

- 阿里云备案文档：<https://help.aliyun.com/zh/icp-filing/>
- 腾讯云 ICP 备案文档：<https://cloud.tencent.com/document/product/243>
- 腾讯云 CVM 创建实例文档：<https://cloud.tencent.com/document/product/213/4855>
- GitHub Pages 自定义域名文档：<https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages>
- Certbot Nginx HTTPS 文档：<https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal>
