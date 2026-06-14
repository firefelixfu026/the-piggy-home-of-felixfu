# Docker Desktop 安装与验证指南

本文用于完成本项目下一阶段 `v0.3.0 数据持久化版本` 的前置准备。v0.3.0 会使用 PostgreSQL，推荐通过 Docker Desktop + Docker Compose 在本地启动数据库。

参考官方文档：

- Docker Desktop Windows 安装文档：<https://docs.docker.com/desktop/setup/install/windows-install/>
- Microsoft WSL 安装文档：<https://learn.microsoft.com/en-us/windows/wsl/install>

## 1. 当前电脑检查结果

我已经在当前环境检查过：

- `docker --version`：未找到，说明 Docker Desktop / Docker CLI 还没有安装好。
- `wsl --version`：能返回 WSL 版本信息，说明 WSL 组件存在。
- `wsl --list --verbose`：没有看到可用 Linux 发行版，建议安装 Ubuntu。

因此你需要做的是：

1. 安装或确认 Ubuntu WSL 发行版。
2. 安装 Docker Desktop。
3. 启动 Docker Desktop，并确认 Docker CLI 可用。

## 2. 安装前确认

你需要确认：

- Windows 10/11，64 位系统。
- BIOS/UEFI 已开启虚拟化。
- 电脑内存建议至少 8GB。
- 能访问 Docker 官方下载地址，或可以使用 `winget`。

Docker 官方文档要求 WSL 2 后端需要 WSL 版本 2.1.5 或以上，并开启 WSL 2 功能。本机 `wsl --version` 已显示 WSL 组件存在，版本看起来满足要求。

## 3. 安装 Ubuntu WSL

用“管理员 PowerShell”执行：

```powershell
wsl --install -d Ubuntu
```

如果提示已经安装 WSL，但没有 Ubuntu，可以先查看可安装发行版：

```powershell
wsl --list --online
```

然后安装 Ubuntu：

```powershell
wsl --install -d Ubuntu
```

安装完成后重启电脑。第一次打开 Ubuntu 时，会要求创建 Linux 用户名和密码。这个密码不是 Windows 密码，后续偶尔会用于 Ubuntu 内部的 `sudo`。

验证：

```powershell
wsl --list --verbose
```

期望看到类似：

```text
  NAME      STATE           VERSION
* Ubuntu    Stopped         2
```

如果 Ubuntu 的 VERSION 是 1，执行：

```powershell
wsl --set-version Ubuntu 2
```

## 4. 安装 Docker Desktop

推荐方式一：官网安装包

1. 打开 Docker 官方 Windows 安装页面：<https://docs.docker.com/desktop/setup/install/windows-install/>
2. 下载 `Docker Desktop Installer.exe`。
3. 双击安装。
4. 安装模式建议选择 `per-user`，通常不需要管理员权限。
5. 配置页面选择 `Use WSL 2 instead of Hyper-V`。
6. 安装完成后启动 Docker Desktop。
7. 第一次启动时接受 Docker Desktop Subscription Service Agreement。

推荐方式二：winget 安装

普通 PowerShell 中执行：

```powershell
winget install -e --id Docker.DockerDesktop
```

如果提示需要管理员权限，就用“管理员 PowerShell”再执行一次。

## 5. Docker Desktop 启动设置

打开 Docker Desktop 后检查：

1. Settings -> General
2. 确认启用 `Use the WSL 2 based engine`
3. Settings -> Resources -> WSL integration
4. 开启 Ubuntu 的集成
5. 点击 `Apply & Restart`

Docker Desktop 必须处于运行状态，命令行里的 `docker` 才能正常连接 Docker Engine。

## 6. 验证 Docker 是否可用

重新打开一个 PowerShell，执行：

```powershell
docker --version
docker compose version
docker run hello-world
```

期望结果：

- `docker --version` 输出 Docker 版本。
- `docker compose version` 输出 Compose 版本。
- `docker run hello-world` 能拉取并运行测试镜像。

如果 `docker run hello-world` 成功，说明 Docker Desktop 已经准备好。

## 7. 项目下一步会用到的操作

Docker 安装完成后，我会为项目增加：

- `docker-compose.yml`
- PostgreSQL 数据库服务
- 数据库账号、密码、库名
- 后端数据库连接配置
- SQLAlchemy 模型
- 初始化示例文章数据

到时候你只需要执行：

```powershell
docker compose up -d
```

然后我会继续改造 FastAPI，让文章、评论、点赞、收藏、点踩全部写入数据库。

## 8. 常见问题

### PowerShell 提示 docker 不是命令

原因通常是 Docker Desktop 没装好，或者装完后没有重新打开 PowerShell。

处理：

1. 确认 Docker Desktop 已启动。
2. 关闭当前 PowerShell。
3. 重新打开 PowerShell。
4. 再执行 `docker --version`。

### Docker Desktop 一直启动失败

优先检查：

- WSL 是否安装了 Ubuntu。
- `wsl --list --verbose` 中 Ubuntu 是否是 VERSION 2。
- BIOS/UEFI 是否开启虚拟化。
- Windows 功能里是否启用了 WSL 和 Virtual Machine Platform。

### 拉取镜像很慢

这属于 Docker 镜像网络问题。先告诉我错误输出，我再判断是否需要配置镜像源或代理。

## 9. 你完成后告诉我什么

请把下面三条命令的输出发给我：

```powershell
docker --version
docker compose version
wsl --list --verbose
```

如果 `docker run hello-world` 成功，也告诉我一声。之后我就可以继续做 `v0.3.0 数据持久化版本`。

