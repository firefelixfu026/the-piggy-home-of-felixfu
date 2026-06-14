# 数据持久化说明

版本：v0.3.0

本项目已接入 PostgreSQL，把文章、评论、点赞、收藏、点踩从静态/内存数据改为数据库读写。

## 1. 本地数据库启动

推荐命令：

```powershell
docker compose up -d postgres
```

如果当前 PowerShell 找不到 `docker` 命令，可以使用完整路径：

```powershell
$env:Path = 'C:\Program Files\Docker\Docker\resources\bin;' + $env:Path
& 'C:\Program Files\Docker\Docker\resources\bin\docker.exe' compose up -d postgres
```

查看容器状态：

```powershell
docker compose ps
```

停止数据库：

```powershell
docker compose down
```

如果要连同本地数据库数据一起删除：

```powershell
docker compose down -v
```

## 2. 数据库连接

开发环境默认连接：

```text
postgresql+psycopg://felix_blog:felix_blog_dev@localhost:5432/felix_blog
```

对应 Docker Compose 配置：

- 数据库：`felix_blog`
- 用户：`felix_blog`
- 密码：`felix_blog_dev`
- 端口：`5432`

## 3. 后端依赖

后端新增依赖：

```text
sqlalchemy
psycopg[binary]
```

安装命令：

```powershell
python -m pip install -r backend\requirements.txt
```

## 4. 数据表

当前 SQLAlchemy 模型包含：

- `users`：用户表，预留邮箱登录和 GitHub OAuth。
- `articles`：文章表。
- `tags`：标签表。
- `article_tags`：文章和标签的关联表。
- `comments`：评论表。
- `reaction_counters`：文章互动计数表，存储点赞、收藏、点踩数量。

## 5. 初始化数据

FastAPI 启动时会自动执行：

1. 创建数据库表。
2. 如果文章表为空，写入 3 篇示例文章。
3. 为每篇文章初始化 `like`、`favorite`、`downvote` 三种互动计数。

这部分代码位于：

- `backend/app/database.py`
- `backend/app/models.py`
- `backend/app/seed.py`

## 6. 当前接口行为

文章列表：

```http
GET /api/articles
```

文章搜索：

```http
GET /api/articles?q=AI
```

提交评论：

```http
POST /api/articles/{article_id}/comments
```

请求体：

```json
{
  "content": "评论内容",
  "authorName": "访客"
}
```

提交互动：

```http
POST /api/articles/{article_id}/reaction
```

请求体：

```json
{
  "type": "like",
  "active": true
}
```

`type` 可选：

- `like`
- `favorite`
- `downvote`

`active=true` 表示增加计数，`active=false` 表示取消并减少计数，最低不会小于 0。

管理后台接口：

```http
POST /api/admin/articles
PUT /api/admin/articles/{article_id}
DELETE /api/admin/articles/{article_id}
```

创建和编辑文章的请求体：

```json
{
  "title": "文章标题",
  "summary": "文章摘要",
  "content": "文章正文",
  "tags": ["React", "FastAPI"],
  "date": "2026-06-14",
  "readTime": "3 min"
}
```

当前管理接口尚未加登录鉴权，后续 v0.5.0 会增加管理员登录和 JWT 保护。

## 7. 验证命令

启动数据库和后端后，执行：

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/articles?q=AI' -UseBasicParsing
```

期望：

- `/api/health` 返回 `version: 0.3.0`
- `/api/health` 返回 `articles: 3`
- `/api/articles?q=AI` 能返回包含 AI 关键词或标签的文章

## 8. 后续改进

当前 v0.3.0 使用 `Base.metadata.create_all()` 自动建表。后续进入多人协作或线上部署前，应加入 Alembic，使用正式数据库迁移管理表结构变化。
