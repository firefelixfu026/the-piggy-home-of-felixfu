from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Article, ReactionCounter, Tag


SEED_ARTICLES = [
    {
        "id": "react-fastapi-mvp",
        "title": "React + FastAPI 个人博客 MVP 搭建记录",
        "summary": "记录个人博客第一版的页面结构、接口规划和前后端分离方式，作为后续 PostgreSQL、登录和部署的基础。",
        "content": "本篇文章聚焦 MVP 阶段：先搭建 React 页面，使用 FastAPI 提供个人信息、文章列表和搜索接口，再逐步接入 PostgreSQL、GitHub Actions 和云服务器部署。",
        "tags": ["React", "FastAPI", "MVP"],
        "date": "2026-06-14",
        "read_time": "5 min",
    },
    {
        "id": "running-and-study",
        "title": "长跑、学习和项目节奏",
        "summary": "把长跑训练里的节奏感迁移到项目推进中，按周拆解任务，稳定积累可展示成果。",
        "content": "个人博客的建设也可以像训练计划一样推进：先有可运行版本，再逐步增加数据库、鉴权、自动化、AI 和小游戏模块。",
        "tags": ["长跑", "学习方法", "计划"],
        "date": "2026-06-14",
        "read_time": "3 min",
    },
    {
        "id": "ai-digest-plan",
        "title": "每日技术新闻和文章 AI 总结计划",
        "summary": "规划 AI 自动化模块：每天抓取技术新闻，自动提炼摘要，并为站内文章生成结构化总结。",
        "content": "AI 自动化模块会分两步实现。第一步展示占位数据和页面入口，第二步接入真实模型和定时任务，第三步缓存摘要结果并形成可检索知识库。",
        "tags": ["AI", "自动化", "技术新闻"],
        "date": "2026-06-14",
        "read_time": "4 min",
    },
]

REACTION_TYPES = ["like", "favorite", "downvote"]


def seed_database(db: Session) -> None:
    if db.scalar(select(Article.id).limit(1)):
        return

    for item in SEED_ARTICLES:
        article = Article(
            id=item["id"],
            title=item["title"],
            summary=item["summary"],
            content=item["content"],
            date=item["date"],
            read_time=item["read_time"],
        )
        article.tags = [_get_or_create_tag(db, tag_name) for tag_name in item["tags"]]
        article.reactions = [
            ReactionCounter(reaction_type=reaction_type, count=0)
            for reaction_type in REACTION_TYPES
        ]
        db.add(article)

    db.commit()


def _get_or_create_tag(db: Session, name: str) -> Tag:
    tag = db.scalar(select(Tag).where(Tag.name == name))
    if tag:
        return tag

    tag = Tag(name=name)
    db.add(tag)
    db.flush()
    return tag

