# IT Training Management System

Self-hosted platform to upload training videos, generate quizzes, build personalized learning paths, and track team progress, with Hermes as the orchestrator.

- Stack: Ubuntu + Docker + Hermes + Open WebUI + Ollama + Qdrant + MinIO + SQLite/Postgres
- Primary interface: Telegram + web dashboard
- Intended use: internal IT upskilling with fully automated ingestion and coaching

## Quick start

```bash
git clone https://github.com/OneByJorah/it-training-system.git
cd it-training-system
cp compose.env.example .env
docker compose up -d
bash scripts/bootstrap.sh
```

## What you get

- Docker Compose for training stack
- Hermes skills for ingestion, quizzes, learning paths, progress tracking, content creation, and Telegram bot
- FastAPI backend with schema
- Setup + bootstrap scripts
- Full docs under `docs/`

## Docs

- `docs/ARCHITECTURE.md`
- `docs/DATA_MODEL.md`
- `docs/BUILD_PLAN.md`

