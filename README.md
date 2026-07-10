# FelixFu Personal Blog

[![CI](https://github.com/firefelixfu026/the-piggy-home-of-felixfu/actions/workflows/ci.yml/badge.svg)](https://github.com/firefelixfu026/the-piggy-home-of-felixfu/actions/workflows/ci.yml)

FelixFu Personal Blog is a full-stack personal website built with React, FastAPI, PostgreSQL, Docker, Nginx, and GitHub Actions.

It started as a personal blog MVP and has grown into a maintainable content platform with article publishing, Markdown and LaTeX rendering, image uploads, comments, account-based interactions, GitHub OAuth login, an admin dashboard, AI-assisted writing, and automatic deployment.

## Live Site

```text
https://www.felixfu.xyz
```

## Tech Stack

- Frontend: React, Vite
- Backend: FastAPI, SQLAlchemy
- Database: PostgreSQL
- Auth: email/password login, GitHub OAuth, token-based authentication
- Deployment: Docker Compose, Nginx, HTTPS
- Automation: GitHub Actions CI and deployment
- AI: local fallback generation plus configurable OpenAI-compatible provider support

## Main Features

- Article list, search, categories, tags, archives, pinned posts, and reading time
- Article detail page with Markdown, LaTeX, and inline images
- Admin-only article creation, editing, deletion, draft status, image upload, and statistics
- Login-gated comments with replies, pagination, length limits, and moderation
- Account-based like, favorite, dislike, and question-mark reactions with de-duplication
- Account center for personal comments and interactions
- GitHub OAuth login and role-based admin permissions
- AI workbench for article ideas, summaries, titles, polishing, continuation, and outlines
- Embedded game page as a personal project showcase
- PostgreSQL persistence and Docker volume-based uploaded image storage
- GitHub Actions automatic test and deployment workflow

## Project Structure

```text
.
├── backend/                 # FastAPI backend
├── frontend/                # React frontend
├── docs/
│   ├── README.md            # Documentation index
│   ├── guides/              # Deployment, database, OAuth, and operations guides
│   └── archive/             # Historical notes and old stage documents
├── scripts/                 # Server and maintenance scripts
├── .github/workflows/       # CI and deployment workflows
├── docker-compose.yml       # Local/server service orchestration
├── .env.example             # Environment variable template
├── CHANGELOG.md             # Release history
└── README.md                # Project overview
```

## Quick Start

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Start PostgreSQL, backend, and frontend with Docker Compose:

```powershell
docker compose up -d --build
```

Open the local site:

```text
http://127.0.0.1:8080
```

Health checks:

```text
http://127.0.0.1:8000/api/health
http://127.0.0.1:8080/api/health
```

For detailed startup and deployment instructions, see [docs/guides/DOCKER_COMPOSE.md](docs/guides/DOCKER_COMPOSE.md).

## Environment Variables

The main environment variables are listed in `.env.example`.

Important production values include:

- `DATABASE_URL`
- `AUTH_SECRET`
- `ADMIN_SETUP_TOKEN`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITHUB_OAUTH_CALLBACK_URL`
- `GITHUB_ADMIN_LOGINS`
- `AI_PROVIDER_NAME`
- `AI_API_STYLE`
- `AI_BASE_URL`
- `AI_MODEL`
- `AI_API_KEY`

Do not commit `.env` or real API keys to the repository.

## AI Provider Notes

The AI module can run in two modes:

- Local fallback mode: works without a real model provider and keeps the writing workflow available.
- Real provider mode: calls an OpenAI-compatible API or a supported relay endpoint.

For an OpenAI-compatible relay such as AICodeMirror, use the provider's SDK-compatible base URL, for example:

```text
https://api.aicodemirror.com/api/codex/backend-api/codex/v1
```

Then set:

```text
AI_API_STYLE=openai
```

The backend will call `/chat/completions` under that base URL.

## Documentation

See [docs/README.md](docs/README.md) for the organized documentation index.

Useful guides:

- [Docker Compose Guide](docs/guides/DOCKER_COMPOSE.md)
- [Database Guide](docs/guides/DATABASE.md)
- [Database Backup Guide](docs/guides/DATABASE_BACKUP.md)
- [GitHub OAuth Setup](docs/guides/GITHUB_OAUTH_APP_SETUP.md)
- [GitHub Actions Deployment](docs/guides/GITHUB_ACTIONS_DEPLOYMENT.md)
- [Server Operations](docs/guides/SERVER_OPERATIONS.md)

## Deployment Summary

The production site runs on an Alibaba Cloud Ubuntu server.

Current deployment shape:

- Nginx handles HTTPS and reverse proxying.
- Docker Compose runs frontend, backend, and PostgreSQL.
- PostgreSQL and uploaded files are persisted with Docker volumes.
- GitHub Actions runs CI on push and triggers deployment after successful checks.

## Security Notes

- Admin routes are protected by backend role checks.
- The admin setup flow requires `ADMIN_SETUP_TOKEN`.
- Visitors cannot comment or react until they log in.
- Reactions are account-based and cannot be counted repeatedly by refreshing the page.
- API keys and OAuth secrets must stay in environment variables.
- Uploaded images are type-restricted before being stored.

## License

This is a personal learning and portfolio project.
