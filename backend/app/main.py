from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import SessionLocal, get_db, init_db
from app.models import Article, Comment, ReactionCounter
from app.seed import REACTION_TYPES, seed_database


app = FastAPI(title="FelixFu Blog API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PROFILE = {
    "name": "付江樊",
    "englishName": "Felix Fu",
    "school": "浙江大学",
    "role": "综合型个人博客 · 学习笔记 · 技术项目",
    "interests": ["长跑", "唱歌", "游戏"],
    "summary": "这里会逐步沉淀学习笔记、技术文章、个人项目、AI 自动化内容和小游戏实验。MVP 阶段先完成可展示结构，后续接入真实登录、数据库和云端部署。",
    "metrics": [
        {"label": "MVP 状态", "value": "v0.3"},
        {"label": "文章方向", "value": "技术/学习"},
        {"label": "扩展模块", "value": "AI + 游戏"},
    ],
}

AI_NEWS = [
    {
        "title": "前后端分离项目优先打通接口契约",
        "source": "Daily Tech Digest",
        "summary": "先固定页面、数据结构和 API 路由，可以降低后续接入数据库和鉴权时的改动成本。",
    },
    {
        "title": "AI 总结模块适合从文章摘要开始",
        "source": "AI Workflow",
        "summary": "MVP 阶段可先保留摘要入口，后续把文章正文发送到模型服务并缓存总结结果。",
    },
]


class CommentIn(BaseModel):
    content: str
    authorName: str | None = None


class ReactionIn(BaseModel):
    type: Literal["like", "favorite", "downvote"]
    active: bool = True


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with SessionLocal() as db:
        seed_database(db)


@app.get("/api/health")
def health(db: Session = Depends(get_db)) -> dict[str, str | int]:
    article_count = len(db.scalars(select(Article.id)).all())
    return {"status": "ok", "version": "0.3.0", "articles": article_count}


@app.get("/api/profile")
def get_profile() -> dict:
    return PROFILE


@app.get("/api/articles")
def list_articles(q: str | None = Query(default=None), db: Session = Depends(get_db)) -> list[dict]:
    articles = _load_articles(db)
    if not q:
        return [_article_to_dict(article) for article in articles]

    keyword = q.strip().lower()
    filtered = [
        article
        for article in articles
        if keyword
        in " ".join(
            [
                article.title,
                article.summary,
                article.content,
                " ".join(tag.name for tag in article.tags),
            ]
        ).lower()
    ]
    return [_article_to_dict(article) for article in filtered]


@app.get("/api/articles/{article_id}")
def get_article(article_id: str, db: Session = Depends(get_db)) -> dict:
    article = _get_article_or_404(db, article_id)
    return _article_to_dict(article)


@app.post("/api/articles/{article_id}/comments")
def create_comment(article_id: str, comment: CommentIn, db: Session = Depends(get_db)) -> dict:
    article = _get_article_or_404(db, article_id)
    content = comment.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Comment content is required")

    db.add(
        Comment(
            article_id=article.id,
            author_name=(comment.authorName or "访客").strip() or "访客",
            content=content,
        )
    )
    db.commit()
    db.refresh(article)
    article = _get_article_or_404(db, article_id)
    return {"articleId": article_id, "comments": [_comment_to_dict(item) for item in article.comments]}


@app.post("/api/articles/{article_id}/reaction")
def create_reaction(article_id: str, reaction: ReactionIn, db: Session = Depends(get_db)) -> dict:
    article = _get_article_or_404(db, article_id)
    counter = _get_or_create_reaction_counter(db, article.id, reaction.type)
    counter.count = max(0, counter.count + (1 if reaction.active else -1))
    db.commit()
    db.refresh(article)
    article = _get_article_or_404(db, article_id)
    return {"articleId": article_id, "reactions": _reaction_counts(article)}


@app.get("/api/ai/news")
def get_ai_news() -> list[dict]:
    return AI_NEWS


@app.get("/api/game/card-war")
def get_card_war_info() -> dict[str, str]:
    return {
        "title": "决斗小游戏",
        "repository": "https://github.com/firefelixfu026/card-war-made-by-class-3",
        "playUrl": "https://firefelixfu026.github.io/card-war-made-by-class-3/",
        "status": "embedded",
    }


def _load_articles(db: Session) -> list[Article]:
    statement = (
        select(Article)
        .options(
            selectinload(Article.tags),
            selectinload(Article.comments),
            selectinload(Article.reactions),
        )
        .order_by(Article.created_at.desc())
    )
    return list(db.scalars(statement).all())


def _get_article_or_404(db: Session, article_id: str) -> Article:
    article = db.scalar(
        select(Article)
        .where(Article.id == article_id)
        .options(
            selectinload(Article.tags),
            selectinload(Article.comments),
            selectinload(Article.reactions),
        )
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def _article_to_dict(article: Article) -> dict:
    return {
        "id": article.id,
        "title": article.title,
        "summary": article.summary,
        "content": article.content,
        "tags": [tag.name for tag in sorted(article.tags, key=lambda item: item.name)],
        "date": article.date,
        "readTime": article.read_time,
        "comments": [_comment_to_dict(comment) for comment in article.comments],
        "reactions": _reaction_counts(article),
    }


def _comment_to_dict(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "authorName": comment.author_name,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat(),
    }


def _reaction_counts(article: Article) -> dict[str, int]:
    counts = {reaction_type: 0 for reaction_type in REACTION_TYPES}
    for reaction in article.reactions:
        counts[reaction.reaction_type] = reaction.count
    return counts


def _get_or_create_reaction_counter(db: Session, article_id: str, reaction_type: str) -> ReactionCounter:
    counter = db.scalar(
        select(ReactionCounter).where(
            ReactionCounter.article_id == article_id,
            ReactionCounter.reaction_type == reaction_type,
        )
    )
    if counter:
        return counter

    counter = ReactionCounter(article_id=article_id, reaction_type=reaction_type, count=0)
    db.add(counter)
    db.flush()
    return counter

