import hmac
import os
import re
from datetime import datetime
from typing import Literal
from urllib.parse import urlencode
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.auth import (
    create_access_token,
    create_oauth_state,
    get_current_user,
    get_optional_current_user,
    hash_password,
    require_admin,
    verify_oauth_state,
    verify_password,
)
from app.database import SessionLocal, get_db, init_db
from app.github_oauth import fetch_github_identity, get_github_authorize_url
from app.models import Article, Comment, ReactionCounter, Tag, User, UserReaction
from app.seed import REACTION_TYPES, seed_database


FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5173").rstrip("/")
ADMIN_SETUP_TOKEN = os.getenv("ADMIN_SETUP_TOKEN", "").strip()
COMMENT_MAX_LENGTH = 300


app = FastAPI(title="FelixFu Blog API", version="0.8.0")

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
        {"label": "MVP 状态", "value": "v0.8"},
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
    type: Literal["like", "favorite", "downvote", "question"]
    active: bool = True


class ArticleIn(BaseModel):
    title: str
    summary: str
    content: str
    tags: list[str] = []
    date: str | None = None
    readTime: str = "3 min"
    status: Literal["published", "draft"] = "published"


class RegisterIn(BaseModel):
    email: str
    password: str
    displayName: str = "Felix Fu"
    setupToken: str = ""


class LoginIn(BaseModel):
    email: str
    password: str


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    with SessionLocal() as db:
        seed_database(db)


@app.get("/api/health")
def health(db: Session = Depends(get_db)) -> dict[str, str | int]:
    article_count = len(db.scalars(select(Article.id)).all())
    return {"status": "ok", "version": "0.8.0", "articles": article_count}


@app.get("/api/profile")
def get_profile() -> dict:
    return PROFILE


@app.get("/api/articles")
def list_articles(
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
) -> list[dict]:
    articles = _load_articles(db)
    if not current_user or current_user.role != "admin":
        articles = [article for article in articles if article.status == "published"]
    if not q:
        return [_article_to_dict(article, current_user) for article in articles]

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
    return [_article_to_dict(article, current_user) for article in filtered]


@app.get("/api/articles/{article_id}")
def get_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
) -> dict:
    article = _get_article_or_404(db, article_id)
    _ensure_article_visible(article, current_user)
    if not current_user or current_user.role != "admin":
        article.view_count = (article.view_count or 0) + 1
        db.commit()
        db.refresh(article)
    return _article_to_dict(article, current_user)


@app.post("/api/articles/{article_id}/comments")
def create_comment(
    article_id: str,
    comment: CommentIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    article = _get_article_or_404(db, article_id)
    _ensure_article_visible(article, current_user)
    content = comment.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Comment content is required")
    if len(content) > COMMENT_MAX_LENGTH:
        raise HTTPException(status_code=400, detail=f"Comment must be {COMMENT_MAX_LENGTH} characters or fewer")

    db.add(
        Comment(
            article_id=article.id,
            author_name=(current_user.display_name or current_user.email or "访客").strip() or "访客",
            content=content,
            status="pending",
        )
    )
    db.commit()
    db.refresh(article)
    article = _get_article_or_404(db, article_id)
    return {
        "articleId": article_id,
        "comments": [_comment_to_dict(item) for item in _public_comments(article)],
        "message": "评论已提交，审核通过后会公开显示",
    }


@app.post("/api/articles/{article_id}/reaction")
def create_reaction(
    article_id: str,
    reaction: ReactionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    article = _get_article_or_404(db, article_id)
    _ensure_article_visible(article, current_user)
    existing = db.scalar(
        select(UserReaction).where(
            UserReaction.user_id == current_user.id,
            UserReaction.article_id == article.id,
            UserReaction.reaction_type == reaction.type,
        )
    )

    if reaction.active and not existing:
        db.add(
            UserReaction(
                user_id=current_user.id,
                article_id=article.id,
                reaction_type=reaction.type,
            )
        )
    elif not reaction.active and existing:
        db.delete(existing)

    db.commit()
    _sync_reaction_counters(db, article.id)
    article = _get_article_or_404(db, article_id)
    return {
        "articleId": article_id,
        "reactions": _reaction_counts(article),
        "viewerReactions": _viewer_reactions(article, current_user),
    }

@app.post("/api/auth/register")
def register_admin(payload: RegisterIn, db: Session = Depends(get_db)) -> dict:
    if db.scalar(select(User.id).where(User.role == "admin")):
        raise HTTPException(status_code=403, detail="Admin account is already initialized")

    _verify_admin_setup_token(payload.setupToken)

    email = _normalize_email(payload.email)
    password = _validate_password(payload.password)
    display_name = payload.displayName.strip() or "Felix Fu"

    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail="Email is already registered")

    user = User(
        email=email,
        display_name=display_name,
        password_hash=hash_password(password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_access_token(user), "user": _user_to_dict(user)}


@app.post("/api/auth/login")
def login(payload: LoginIn, db: Session = Depends(get_db)) -> dict:
    email = _normalize_email(payload.email)
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"token": create_access_token(user), "user": _user_to_dict(user)}


@app.get("/api/auth/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict:
    return {"user": _user_to_dict(current_user)}


@app.get("/api/auth/github/start")
def start_github_login() -> RedirectResponse:
    try:
        return RedirectResponse(get_github_authorize_url(create_oauth_state("/admin")))
    except HTTPException as exc:
        return _frontend_auth_redirect(error=str(exc.detail))


@app.get("/api/auth/github/callback")
def github_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    if error:
        return _frontend_auth_redirect(error=error)
    if not code or not state:
        return _frontend_auth_redirect(error="GitHub callback is missing code or state")

    try:
        verify_oauth_state(state)
        profile, email = fetch_github_identity(code)
        user = _upsert_github_user(db, profile, email)
        return _frontend_auth_redirect(token=create_access_token(user))
    except HTTPException as exc:
        return _frontend_auth_redirect(error=str(exc.detail))


@app.post("/api/admin/articles")
def create_admin_article(
    payload: ArticleIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict:
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Article title is required")

    article = Article(
        id=_generate_article_id(db, title),
        title=title,
        summary=_required_text(payload.summary, "Article summary is required"),
        content=_required_text(payload.content, "Article content is required"),
        date=(payload.date or datetime.utcnow().date().isoformat()).strip(),
        read_time=(payload.readTime or "3 min").strip(),
        status=payload.status,
    )
    article.tags = [_get_or_create_tag(db, tag_name) for tag_name in _clean_tags(payload.tags)]
    article.reactions = [
        ReactionCounter(reaction_type=reaction_type, count=0)
        for reaction_type in REACTION_TYPES
    ]
    db.add(article)
    db.commit()
    return _article_to_dict(_get_article_or_404(db, article.id), current_user)


@app.put("/api/admin/articles/{article_id}")
def update_admin_article(
    article_id: str,
    payload: ArticleIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict:
    article = _get_article_or_404(db, article_id)
    article.title = _required_text(payload.title, "Article title is required")
    article.summary = _required_text(payload.summary, "Article summary is required")
    article.content = _required_text(payload.content, "Article content is required")
    article.date = (payload.date or article.date).strip()
    article.read_time = (payload.readTime or article.read_time).strip()
    article.status = payload.status
    article.tags = [_get_or_create_tag(db, tag_name) for tag_name in _clean_tags(payload.tags)]
    db.commit()
    return _article_to_dict(_get_article_or_404(db, article.id), current_user)


@app.delete("/api/admin/articles/{article_id}")
def delete_admin_article(
    article_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict[str, str]:
    article = _get_article_or_404(db, article_id)
    db.delete(article)
    db.commit()
    return {"status": "deleted", "articleId": article_id}


@app.get("/api/admin/comments")
def list_admin_comments(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> list[dict]:
    comments = db.scalars(
        select(Comment)
        .options(selectinload(Comment.article))
        .order_by(Comment.created_at.desc())
    ).all()
    return [_admin_comment_to_dict(comment) for comment in comments]


@app.delete("/api/admin/comments/{comment_id}")
def delete_admin_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict[str, int | str]:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
    return {"status": "deleted", "commentId": comment_id}


@app.post("/api/admin/comments/{comment_id}/approve")
def approve_admin_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
) -> dict:
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    comment.status = "approved"
    db.commit()
    db.refresh(comment)
    return _admin_comment_to_dict(comment)


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
            selectinload(Article.user_reactions),
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
            selectinload(Article.user_reactions),
        )
    )
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


def _article_to_dict(article: Article, current_user: User | None = None) -> dict:
    return {
        "id": article.id,
        "title": article.title,
        "summary": article.summary,
        "content": article.content,
        "tags": [tag.name for tag in sorted(article.tags, key=lambda item: item.name)],
        "date": article.date,
        "readTime": article.read_time,
        "status": article.status,
        "viewCount": article.view_count or 0,
        "comments": [_comment_to_dict(comment) for comment in _visible_comments(article, current_user)],
        "reactions": _reaction_counts(article),
        "viewerReactions": _viewer_reactions(article, current_user),
    }


def _ensure_article_visible(article: Article, current_user: User | None) -> None:
    if article.status == "published":
        return
    if current_user and current_user.role == "admin":
        return
    raise HTTPException(status_code=404, detail="Article not found")


def _visible_comments(article: Article, current_user: User | None) -> list[Comment]:
    if current_user and current_user.role == "admin":
        return sorted(article.comments, key=lambda item: item.created_at)
    return _public_comments(article)


def _public_comments(article: Article) -> list[Comment]:
    return sorted(
        [comment for comment in article.comments if comment.status == "approved"],
        key=lambda item: item.created_at,
    )


def _comment_to_dict(comment: Comment) -> dict:
    return {
        "id": comment.id,
        "authorName": comment.author_name,
        "content": comment.content,
        "status": comment.status,
        "createdAt": comment.created_at.isoformat(),
    }


def _admin_comment_to_dict(comment: Comment) -> dict:
    return {
        **_comment_to_dict(comment),
        "articleId": comment.article_id,
        "articleTitle": comment.article.title if comment.article else "",
    }


def _reaction_counts(article: Article) -> dict[str, int]:
    counts = {reaction_type: 0 for reaction_type in REACTION_TYPES}
    for reaction in article.reactions:
        counts[reaction.reaction_type] = reaction.count
    return counts


def _viewer_reactions(article: Article, current_user: User | None) -> dict[str, bool]:
    selected = {reaction_type: False for reaction_type in REACTION_TYPES}
    if not current_user:
        return selected

    for reaction in article.user_reactions:
        if reaction.user_id == current_user.id and reaction.reaction_type in selected:
            selected[reaction.reaction_type] = True
    return selected


def _sync_reaction_counters(db: Session, article_id: str) -> None:
    for reaction_type in REACTION_TYPES:
        counter = _get_or_create_reaction_counter(db, article_id, reaction_type)
        counter.count = len(
            db.scalars(
                select(UserReaction.id).where(
                    UserReaction.article_id == article_id,
                    UserReaction.reaction_type == reaction_type,
                )
            ).all()
        )
    db.commit()


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


def _get_or_create_tag(db: Session, name: str) -> Tag:
    tag = db.scalar(select(Tag).where(Tag.name == name))
    if tag:
        return tag

    tag = Tag(name=name)
    db.add(tag)
    db.flush()
    return tag


def _required_text(value: str, message: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail=message)
    return cleaned


def _verify_admin_setup_token(value: str) -> None:
    if not ADMIN_SETUP_TOKEN:
        raise HTTPException(status_code=403, detail="Admin setup is disabled")
    if not hmac.compare_digest(value.strip(), ADMIN_SETUP_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid admin setup token")


def _normalize_email(value: str) -> str:
    email = value.strip().lower()
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=400, detail="A valid email is required")
    return email


def _validate_password(value: str) -> str:
    if len(value) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    return value


def _upsert_github_user(db: Session, profile: dict, email: str | None) -> User:
    github_id = str(profile.get("id") or "").strip()
    login = str(profile.get("login") or "").strip()
    if not github_id or not login:
        raise HTTPException(status_code=400, detail="GitHub profile is missing required fields")

    normalized_email = _github_email(login, email)
    display_name = (profile.get("name") or login).strip()
    avatar_url = profile.get("avatar_url")
    should_be_admin = _is_configured_github_admin(login, normalized_email)

    user = db.scalar(select(User).where(User.github_id == github_id))
    if not user:
        user = db.scalar(select(User).where(User.email == normalized_email))
        if user and user.github_id and user.github_id != github_id:
            raise HTTPException(status_code=409, detail="This email is linked to another GitHub account")

    if user:
        user.github_id = github_id
        user.email = user.email or normalized_email
        user.display_name = display_name
        user.avatar_url = avatar_url
        if should_be_admin:
            user.role = "admin"
    else:
        user = User(
            email=normalized_email,
            github_id=github_id,
            display_name=display_name,
            avatar_url=avatar_url,
            role="admin" if should_be_admin else "reader",
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    return user


def _github_email(login: str, email: str | None) -> str:
    if email and email.strip():
        return email.strip().lower()
    return f"{login.lower()}@users.noreply.github.com"


def _is_configured_github_admin(login: str, email: str) -> bool:
    admin_logins = _split_env_values("GITHUB_ADMIN_LOGINS")
    admin_emails = _split_env_values("GITHUB_ADMIN_EMAILS")
    return login.lower() in admin_logins or email.lower() in admin_emails


def _split_env_values(name: str) -> set[str]:
    return {
        item.strip().lower()
        for item in os.getenv(name, "").split(",")
        if item.strip()
    }


def _frontend_auth_redirect(token: str | None = None, error: str | None = None) -> RedirectResponse:
    params = {"auth": "github"}
    if token:
        params["token"] = token
    if error:
        params["error"] = error
    return RedirectResponse(f"{FRONTEND_ORIGIN}/#{urlencode(params)}")


def _user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "displayName": user.display_name,
        "role": user.role,
        "avatarUrl": user.avatar_url,
        "githubLinked": bool(user.github_id),
    }


def _clean_tags(tags: list[str]) -> list[str]:
    seen: set[str] = set()
    cleaned_tags: list[str] = []
    for tag in tags:
        cleaned = tag.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            cleaned_tags.append(cleaned)
    return cleaned_tags


def _generate_article_id(db: Session, title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        slug = f"article-{datetime.utcnow().strftime('%Y%m%d')}"

    candidate = slug
    while db.get(Article, candidate):
        candidate = f"{slug}-{uuid4().hex[:6]}"
    return candidate
