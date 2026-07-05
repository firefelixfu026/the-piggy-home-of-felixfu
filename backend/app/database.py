import os
from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://felix_blog:felix_blog_dev@localhost:5432/felix_blog",
)


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    _ensure_schema_updates()


def _ensure_schema_updates() -> None:
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    table_names = inspector.get_table_names()
    user_columns = {column["name"] for column in inspector.get_columns("users")}
    article_columns = {column["name"] for column in inspector.get_columns("articles")} if "articles" in table_names else set()
    comment_columns = {column["name"] for column in inspector.get_columns("comments")} if "comments" in table_names else set()
    with engine.begin() as connection:
        if "password_hash" not in user_columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)"))
        if "articles" in table_names and "status" not in article_columns:
            connection.execute(text("ALTER TABLE articles ADD COLUMN status VARCHAR(20) DEFAULT 'published' NOT NULL"))
        if "articles" in table_names and "view_count" not in article_columns:
            connection.execute(text("ALTER TABLE articles ADD COLUMN view_count INTEGER DEFAULT 0 NOT NULL"))
        if "comments" in table_names and "status" not in comment_columns:
            connection.execute(text("ALTER TABLE comments ADD COLUMN status VARCHAR(20) DEFAULT 'approved' NOT NULL"))

        connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations ("
                "name VARCHAR(120) PRIMARY KEY, "
                "applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
            )
        )
        reaction_reset_done = connection.execute(
            text("SELECT name FROM schema_migrations WHERE name = 'reset_reactions_v1_2_3'")
        ).first()
        if not reaction_reset_done:
            connection.execute(text("DELETE FROM user_reactions"))
            connection.execute(text("UPDATE reaction_counters SET count = 0"))
            connection.execute(text("INSERT INTO schema_migrations (name) VALUES ('reset_reactions_v1_2_3')"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
