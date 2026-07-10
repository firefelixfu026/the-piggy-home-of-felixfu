# 数据库备份与恢复指南

版本：v1.0.0
更新时间：2026-07-04

本文档记录 FelixFu 个人博客线上 PostgreSQL 数据库的备份、恢复和日常检查流程。

当前线上结构：

```text
服务器：阿里云中国香港 Ubuntu 22.04
项目目录：/opt/felixfu-blog
数据库容器：felixfu_blog_postgres
数据库：felix_blog
用户：felix_blog
部署方式：Docker Compose
```

## 1. 为什么现在必须做备份

网站上线后，文章、评论、点赞、收藏、点踩、管理员账号和 GitHub OAuth 用户绑定信息都会写入 PostgreSQL。

如果没有备份，以下情况会导致数据丢失：

- 误执行 `docker compose down -v`。
- 服务器磁盘损坏。
- 数据库迁移或代码升级失败。
- 手动删除了文章或用户数据。

## 2. 手动备份

SSH 进入服务器后执行：

```bash
cd /opt/felixfu-blog
mkdir -p backups/postgres
BACKUP_FILE="backups/postgres/felix_blog_$(date +%Y%m%d_%H%M%S).sql"
docker compose exec -T postgres pg_dump -U felix_blog -d felix_blog > "$BACKUP_FILE"
gzip "$BACKUP_FILE"
ls -lh backups/postgres
```

成功后会生成类似：

```text
backups/postgres/felix_blog_20260704_021500.sql.gz
```

## 3. 使用脚本备份

仓库提供脚本：

```text
scripts/backup-postgres.sh
```

首次在服务器执行：

```bash
cd /opt/felixfu-blog
chmod +x scripts/backup-postgres.sh
./scripts/backup-postgres.sh
```

脚本会：

- 创建 `backups/postgres` 目录。
- 使用 `pg_dump` 导出数据库。
- 压缩为 `.sql.gz`。
- 自动删除 14 天以前的备份。
- 打印最新备份文件路径。

## 4. 查看备份

```bash
cd /opt/felixfu-blog
ls -lh backups/postgres
```

建议至少保留最近 7-14 天备份。

## 5. 下载备份到本地

在本机 PowerShell 中执行，示例：

```powershell
scp admin@47.242.176.227:/opt/felixfu-blog/backups/postgres/felix_blog_YYYYMMDD_HHMMSS.sql.gz .
```

把文件名替换成服务器上实际生成的备份文件名。

## 6. 恢复前注意

恢复数据库会覆盖当前线上数据。恢复前必须确认：

1. 已经额外备份当前数据库。
2. 确认要恢复的 `.sql` 或 `.sql.gz` 文件正确。
3. 确认网站可以短暂停止写入。

建议恢复前先做一次当前数据备份：

```bash
cd /opt/felixfu-blog
./scripts/backup-postgres.sh
```

## 7. 从 `.sql.gz` 恢复

假设备份文件是：

```text
backups/postgres/felix_blog_20260704_021500.sql.gz
```

执行：

```bash
cd /opt/felixfu-blog
gunzip -c backups/postgres/felix_blog_20260704_021500.sql.gz > /tmp/felix_restore.sql
docker compose exec -T postgres psql -U felix_blog -d felix_blog < /tmp/felix_restore.sql
rm /tmp/felix_restore.sql
```

如果需要更干净地恢复，先清空 public schema：

```bash
cd /opt/felixfu-blog
docker compose exec -T postgres psql -U felix_blog -d felix_blog -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
gunzip -c backups/postgres/felix_blog_20260704_021500.sql.gz > /tmp/felix_restore.sql
docker compose exec -T postgres psql -U felix_blog -d felix_blog < /tmp/felix_restore.sql
rm /tmp/felix_restore.sql
docker compose restart backend
```

## 8. 自动每日备份

先确认脚本可执行：

```bash
cd /opt/felixfu-blog
chmod +x scripts/backup-postgres.sh
./scripts/backup-postgres.sh
```

编辑 crontab：

```bash
crontab -e
```

加入每天凌晨 3:30 自动备份：

```text
30 3 * * * cd /opt/felixfu-blog && ./scripts/backup-postgres.sh >> backups/postgres/backup.log 2>&1
```

查看日志：

```bash
tail -n 50 /opt/felixfu-blog/backups/postgres/backup.log
```

## 9. 备份健康检查

每周检查一次：

```bash
cd /opt/felixfu-blog
ls -lh backups/postgres | tail
```

确认：

- 最近一天有新备份。
- 备份文件大小不是 0。
- `backup.log` 没有明显错误。

## 10. 不要做的事

不要轻易执行：

```bash
docker compose down -v
```

`-v` 会删除 PostgreSQL volume，等于清空数据库。

如果只是重启服务，使用：

```bash
docker compose restart
```

如果只是更新代码，使用：

```bash
git pull
docker compose up -d --build
```
