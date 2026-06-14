# GitHub 推送问题排查与替代方案

当前本地仓库已经绑定远程仓库：

```text
https://github.com/firefelixfu026/the-piggy-home-of-felixfu.git
```

当前状态：Git for Windows 已通过 Clash 代理恢复 GitHub 访问。

本仓库当前使用的本地 Git 代理配置：

```text
http.proxy=http://127.0.0.1:7897
https.proxy=http://127.0.0.1:7897
```

注意：这是当前仓库的 local 配置，存放在 `.git/config`，不会提交到 GitHub。

## 1. 已排查结果

我已经做过这些检查：

- `https://github.com`：PowerShell 可以访问，返回 200。
- `https://api.github.com`：PowerShell 可以访问，返回 200。
- GitHub Pages 小游戏页面：可以访问，返回 200。
- `git ls-remote origin refs/heads/main`：失败。
- `git push`：失败。
- Git 代理配置：没有配置 `http.proxy` 或 `https.proxy`。
- WinHTTP 代理：Direct access，没有代理。
- Git SSL 后端：已经是 `schannel`。

Git 的详细日志显示：

```text
github.com resolved to 20.205.243.166
Trying 20.205.243.166:443...
connect timed out
```

结论：浏览器/PowerShell 能访问 GitHub，但 Git for Windows 自己连接 `github.com:443` 超时。当前更像是网络出口、代理、校园网、VPN 或防火墙策略对 Git 进程的连接有限制。

已采用的解决方案：让 Git 使用 Clash 的本地 HTTP 代理 `127.0.0.1:7897`，随后 `git ls-remote` 和 `git push` 均可成功执行。

## 2. 最推荐方案：让 Git 使用你的代理

如果你电脑上开了 Clash、V2Ray、VPN、校园网代理等，请告诉我代理地址和端口。当前使用的是 Clash `127.0.0.1:7897`。

常见本地代理端口：

- `127.0.0.1:7890`
- `127.0.0.1:7897`
- `127.0.0.1:1080`
- `127.0.0.1:10808`

当前已在本仓库执行：

```powershell
git config --local http.proxy http://127.0.0.1:7897
git config --local https.proxy http://127.0.0.1:7897
git ls-remote origin refs/heads/main
git push
```

如果以后要改成 SOCKS5 代理，可以使用：

```powershell
git config --local http.proxy socks5h://127.0.0.1:7897
git config --local https.proxy socks5h://127.0.0.1:7897
git ls-remote origin refs/heads/main
git push
```

如果不希望当前仓库继续使用代理，可以清除：

```powershell
git config --local --unset http.proxy
git config --local --unset https.proxy
```

## 3. 备选方案：使用 GitHub Desktop

如果你不想处理命令行网络，可以安装 GitHub Desktop：

<https://desktop.github.com/>

安装后：

1. 登录 GitHub 账号 `felixfu026`。
2. File -> Add local repository。
3. 选择当前项目目录：

```text
E:\FelixFu\document\网站\FelixFu
```

4. GitHub Desktop 会识别本地已有提交。
5. 点击 Push origin。

如果 GitHub Desktop 能推送，说明它使用的网络路径和 Git 命令行不同；后续我仍然可以继续本地开发，你用 GitHub Desktop 点 Push。

## 4. 备选方案：使用 GitHub API

PowerShell 目前可以访问 `https://api.github.com`。理论上可以通过 GitHub REST API 创建 commit 并更新分支，但这需要你提供 GitHub Personal Access Token。

不建议优先用这个方案，因为：

- Token 是敏感信息。
- 需要 `Contents: Read and write` 权限。
- 操作复杂度高于正常 `git push`。

只有在 Git 命令行和 GitHub Desktop 都不可用时，再考虑这个方案。

## 5. 你现在需要告诉我什么

如果后续再次推送失败，请先确认 Clash 仍在运行，且端口仍是 `7897`。如果端口变化，把新端口告诉我即可。
