# GitHub Actions 自动部署指南

版本：v1.1.0
更新时间：2026-07-04

本文档记录 FelixFu 个人博客的 GitHub Actions 自动部署方案。

目标：

```text
本地修改代码 -> 推送 GitHub main -> CI 通过 -> GitHub Actions 自动 SSH 到服务器 -> git pull -> docker compose up -d --build -> 验证服务
```

当前服务器：

```text
正式地址：https://www.felixfu.xyz
服务器 IP：47.242.176.227
SSH 用户：admin
部署目录：/opt/felixfu-blog
```

## 1. 已新增文件

```text
.github/workflows/deploy.yml
scripts/deploy-production.sh
```

`deploy.yml` 会在 `CI` workflow 成功后自动运行，也支持在 GitHub Actions 页面手动触发。

`scripts/deploy-production.sh` 是服务器上的实际部署脚本，也可以手动执行。

## 2. 生成部署 SSH key

在你的本机 PowerShell 执行：

```powershell
ssh-keygen -t ed25519 -C "github-actions-felixfu-blog" -f "$env:USERPROFILE\.ssh\felixfu_blog_deploy_key"
```

一路回车即可，不建议给这个自动部署 key 设置 passphrase。

生成后会得到：

```text
C:\Users\你的用户名\.ssh\felixfu_blog_deploy_key
C:\Users\你的用户名\.ssh\felixfu_blog_deploy_key.pub
```

## 3. 把 public key 加到服务器

先在本机查看 public key：

```powershell
Get-Content "$env:USERPROFILE\.ssh\felixfu_blog_deploy_key.pub"
```

复制输出内容。

登录服务器后执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

把 public key 粘贴进去，保存退出，然后执行：

```bash
chmod 600 ~/.ssh/authorized_keys
```

## 4. 测试 key 登录

在本机 PowerShell 执行：

```powershell
ssh -i "$env:USERPROFILE\.ssh\felixfu_blog_deploy_key" admin@47.242.176.227
```

如果可以免密码登录，说明 key 配置成功。

## 5. 配置 GitHub Secrets

进入 GitHub 仓库：

```text
Settings -> Secrets and variables -> Actions -> New repository secret
```

添加：

```text
DEPLOY_HOST=47.242.176.227
DEPLOY_USER=admin
DEPLOY_PORT=22
DEPLOY_PATH=/opt/felixfu-blog
DEPLOY_SSH_KEY=私钥内容
```

私钥内容查看方式：

```powershell
Get-Content "$env:USERPROFILE\.ssh\felixfu_blog_deploy_key" -Raw
```

复制完整内容，包括：

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

注意：不要把私钥提交到 GitHub 仓库，也不要发到聊天里。

## 6. 手动测试部署 workflow

到 GitHub 仓库：

```text
Actions -> Deploy -> Run workflow
```

选择 `main` 后运行。

成功标准：

- `Validate deployment secrets` 通过。
- `Configure SSH` 通过。
- `Deploy on server` 通过。
- 服务器上 `docker compose ps` 显示服务正常。
- `https://www.felixfu.xyz` 可访问。

## 7. 日常使用

以后正常流程：

```powershell
git add .
git commit -m "你的提交信息"
git push
```

GitHub Actions 会自动：

1. 运行 CI。
2. CI 成功后运行 Deploy。
3. 服务器自动拉取 main 并重建服务。

## 8. 手动部署备用方案

如果 GitHub Actions 临时失败，可 SSH 到服务器执行：

```bash
cd /opt/felixfu-blog
git pull
chmod +x scripts/deploy-production.sh
./scripts/deploy-production.sh
```

## 9. 安全注意

- `DEPLOY_SSH_KEY` 只放在 GitHub Secrets。
- 不要把私钥写入仓库。
- 部署 key 建议只用于这台服务器。
- 如果怀疑 key 泄露，删除服务器 `authorized_keys` 中对应 public key，并在 GitHub Secrets 中删除 `DEPLOY_SSH_KEY`。
