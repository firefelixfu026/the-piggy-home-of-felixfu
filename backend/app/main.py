from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="FelixFu Blog API", version="0.1.0")

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
        {"label": "MVP 状态", "value": "v0.1"},
        {"label": "文章方向", "value": "技术/学习"},
        {"label": "扩展模块", "value": "AI + 游戏"},
    ],
}

ARTICLES = [
    {
        "id": "react-fastapi-mvp",
        "title": "React + FastAPI 个人博客 MVP 搭建记录",
        "summary": "记录个人博客第一版的页面结构、接口规划和前后端分离方式，作为后续 PostgreSQL、登录和部署的基础。",
        "content": "本篇文章聚焦 MVP 阶段：先搭建 React 页面，使用 FastAPI 提供个人信息、文章列表和搜索接口，再逐步接入 PostgreSQL、GitHub Actions 和云服务器部署。",
        "tags": ["React", "FastAPI", "MVP"],
        "date": "2026-06-14",
        "readTime": "5 min",
    },
    {
        "id": "running-and-study",
        "title": "长跑、学习和项目节奏",
        "summary": "把长跑训练里的节奏感迁移到项目推进中，按周拆解任务，稳定积累可展示成果。",
        "content": "个人博客的建设也可以像训练计划一样推进：先有可运行版本，再逐步增加数据库、鉴权、自动化、AI 和小游戏模块。",
        "tags": ["长跑", "学习方法", "计划"],
        "date": "2026-06-14",
        "readTime": "3 min",
    },
    {
        "id": "ai-digest-plan",
        "title": "每日技术新闻和文章 AI 总结计划",
        "summary": "规划 AI 自动化模块：每天抓取技术新闻，自动提炼摘要，并为站内文章生成结构化总结。",
        "content": "AI 自动化模块会分两步实现。第一步展示占位数据和页面入口，第二步接入真实模型和定时任务，第三步缓存摘要结果并形成可检索知识库。",
        "tags": ["AI", "自动化", "技术新闻"],
        "date": "2026-06-14",
        "readTime": "4 min",
    },
]

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

COMMENTS: dict[str, list[str]] = {
    "react-fastapi-mvp": ["第一版先把前后端结构跑起来，后续再接数据库。"]
}

REACTIONS: dict[str, dict[str, int]] = {}


class CommentIn(BaseModel):
    content: str


class ReactionIn(BaseModel):
    type: Literal["like", "favorite", "downvote"]


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


@app.get("/api/profile")
def get_profile() -> dict:
    return PROFILE


@app.get("/api/articles")
def list_articles(q: str | None = Query(default=None)) -> list[dict]:
    if not q:
        return ARTICLES

    keyword = q.strip().lower()
    return [
        article
        for article in ARTICLES
        if keyword in " ".join(
            [
                article["title"],
                article["summary"],
                article["content"],
                " ".join(article["tags"]),
            ]
        ).lower()
    ]


@app.get("/api/articles/{article_id}")
def get_article(article_id: str) -> dict:
    article = next((item for item in ARTICLES if item["id"] == article_id), None)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return {**article, "comments": COMMENTS.get(article_id, [])}


@app.post("/api/articles/{article_id}/comments")
def create_comment(article_id: str, comment: CommentIn) -> dict:
    if not any(item["id"] == article_id for item in ARTICLES):
        raise HTTPException(status_code=404, detail="Article not found")

    content = comment.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Comment content is required")

    COMMENTS.setdefault(article_id, []).append(content)
    return {"articleId": article_id, "comments": COMMENTS[article_id]}


@app.post("/api/articles/{article_id}/reaction")
def create_reaction(article_id: str, reaction: ReactionIn) -> dict:
    if not any(item["id"] == article_id for item in ARTICLES):
        raise HTTPException(status_code=404, detail="Article not found")

    current = REACTIONS.setdefault(article_id, {"like": 0, "favorite": 0, "downvote": 0})
    current[reaction.type] += 1
    return {"articleId": article_id, "reactions": current}


@app.get("/api/ai/news")
def get_ai_news() -> list[dict]:
    return AI_NEWS


@app.get("/api/game/card-war")
def get_card_war_info() -> dict[str, str]:
    return {
        "title": "决斗小游戏",
        "repository": "https://github.com/firefelixfu026/card-war-made-by-class-3",
        "status": "pending-integration",
    }

