from sqlalchemy import select
from sqlalchemy.orm import Session

from app.legacy_notes import LEGACY_NOTE_ARTICLES
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

ALL_SEED_ARTICLES = [*SEED_ARTICLES, *LEGACY_NOTE_ARTICLES]

REACTION_TYPES = ["like", "favorite", "downvote", "question"]

LEGACY_CONTENT_REPLACEMENTS = {
    "https://zju-xlab.feishu.cn/space/api/box/stream/download/asynccode/?code=ZTBlNjU5NTZiZjY5OWUwOGQ1YThkMjM0MGNkMjRlZGNfSDZyVGFGMktvWmVaczlQQU5RVGFSU0N4OXhTeGFjenFfVG9rZW46Rmx0Q2JsQ2xnb0JoTGh4bHpCNWM0bUY3bkpnXzE3Nzc1MTgyNDA6MTc3NzUyMTg0MF9WNA": "/articles/git-workflow.svg",
}


def seed_database(db: Session) -> None:
    has_changes = False
    for item in ALL_SEED_ARTICLES:
        existing_article = db.get(Article, item["id"])
        if existing_article:
            normalized_content = _normalize_seed_content(existing_article.content or "")
            if normalized_content != existing_article.content:
                existing_article.content = normalized_content
                has_changes = True
            continue

        article = Article(
            id=item["id"],
            title=item["title"],
            summary=item["summary"],
            content=_normalize_seed_content(item["content"]),
            date=item["date"],
            read_time=item["read_time"],
            status=item.get("status", "published"),
        )
        article.tags = [_get_or_create_tag(db, tag_name) for tag_name in item["tags"]]
        article.reactions = [
            ReactionCounter(reaction_type=reaction_type, count=0)
            for reaction_type in REACTION_TYPES
        ]
        db.add(article)
        has_changes = True

    if has_changes:
        db.commit()


def _normalize_seed_content(content: str) -> str:
    for old_value, new_value in LEGACY_CONTENT_REPLACEMENTS.items():
        content = content.replace(old_value, new_value)
    return content


def _get_or_create_tag(db: Session, name: str) -> Tag:
    tag = db.scalar(select(Tag).where(Tag.name == name))
    if tag:
        return tag

    tag = Tag(name=name)
    db.add(tag)
    db.flush()
    return tag
