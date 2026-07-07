# INTENT.md — J1-PIPELINE Phase -1 (ORACLE)

**Repository:** `OneByJorah/LearnForge`
**Analysis Date:** 2026-07-05
**Analyst:** J1-PIPELINE ORACLE (read-only)
**Status:** Intent Reconstructed

---

## What This System Does

**LearnForge** (formerly IT Training System) is a self-hosted IT training management platform. It provides structured learning paths, automated AI-generated quizzes, progress tracking, and video ingestion — all running locally via Docker Compose with no external SaaS dependencies.

### Service Table

| Service | Role | Port | Technology |
|---------|------|------|------------|
| `training-api` | FastAPI backend — REST API for users, videos, quizzes, learning paths, events, Telegram webhook | `8080` | Python, FastAPI, SQLAlchemy |
| `ollama` | Local LLM inference — quiz generation, summarization, semantic Q&A | `11434` | Ollama (llama3) |
| `qdrant` | Vector store — semantic search over training content | `6333` | Qdrant |
| `minio` | S3-compatible object storage — training video/media files | `9000` (API), `9001` (Console) | MinIO |

### Operational Role

The system is consumed by:
- **Trainees** — access learning paths, watch videos, take quizzes, track progress
- **Managers** — view team overview dashboards, monitor completion rates and scores
- **Telegram Bot users** — interact via `/my_training`, `/next_lesson`, `/quiz`, `/ask`, `/team_progress` commands
- **Hermes Agent** — orchestrates training workflows via 6 skill definitions (ingestion, quiz generation, learning path engine, progress tracking, content creation, Telegram bot)

---

## Why This Was Built

### Real Problem

Organizations need to deliver IT training to their teams — onboarding new engineers, upskilling existing staff, maintaining compliance knowledge. Commercial training platforms (Docebo, TalentLMS, LearnUpon, 360Learning) are expensive on a per-seat basis, require data to leave the organization's infrastructure, and offer limited customization for AI-powered features like auto-generated quizzes from internal training videos.

### Why Existing Tools Were Insufficient

- **SaaS training platforms** (Docebo, TalentLMS, Cornerstone) — per-seat licensing costs scale poorly for growing teams; data residency and privacy concerns for sensitive internal training content; limited API surface for custom automation.
- **LMS-only solutions** (Moodle, Canvas) — heavy, PHP-based, require significant administration; no native AI/LLM integration for auto-quiz generation or semantic search over video content.
- **Video platforms** (YouTube, Vimeo) — no structured learning paths, no progress tracking, no quiz capabilities.
- **Manual training** — no scalability, no audit trail, no standardized assessment.

### What Triggered Development

The initial commit (`a075316` — "Initial training system design") created the core schema, Docker Compose stack, and FastAPI skeleton. Development was triggered by the need for a lightweight, self-hosted training platform that could:
1. Ingest internal training videos and auto-transcribe them (via Whisper/Ollama)
2. Generate quizzes automatically from video transcripts
3. Track individual and team progress
4. Integrate with Telegram for notifications and interaction
5. Be orchestrated by Hermes Agent for automated workflows

The repo was built as part of the **JorahOne LLC** ecosystem, where Hermes Agent (the organization's AI agent platform) needed a training management subsystem to onboard and upskill team members.

### Ecosystem Fit

```
JorahOne / OneByJorah Ecosystem
├── Hermes Agent OS              — AI agent orchestration platform
├── LearnForge                   — Training management (this repo)
│   ├── Hermes Skills (6)        — Workflow automation for training pipeline
│   ├── FastAPI Backend          — REST API
│   ├── Ollama                   — Local LLM inference
│   ├── Qdrant                   — Vector search
│   └── MinIO                    — Media storage
├── Other JorahOne repos         — Broader infrastructure
```

The 6 Hermes skills (`training-ingestion`, `quiz-generator`, `learning-path-engine`, `progress-tracker`, `content-creator`, `telegram-training-bot`) define the automated workflows that Hermes Agent executes against this system. The `ops/hermes-wiring.md` file explicitly documents the integration points.

---

## Operational Classification

**Classification: PROTOTYPE / BETA**

Evidence:
- **Version**: `0.2.0` (declared in `api/app.py` — pre-1.0, early stage)
- **CI/CD**: Single GitHub Actions workflow that only lints the Docker Compose file — no test execution, no deployment pipeline, no security scanning
- **Health checks**: No health checks defined in `docker-compose.yml` (no `healthcheck` stanza on any service)
- **Database**: Defaults to SQLite (`sqlite:///./app.db`) — Postgres mentioned as future upgrade path but not configured
- **Documentation**: Several docs are placeholder/stub content (`docs/overview.md`, `docs/setup.md`, `docs/observability.md`, `docs/composer-cli.md` contain incomplete or garbled text)
- **AGENTS.md**: Contains only a garbled 2-line fragment — not a real agent configuration
- **Monitoring**: No observability stack (no Prometheus, Grafana, logging aggregator)
- **Backup**: No backup strategy documented
- **Secrets**: Default credentials in `.env.example` (`changeme`, `admin`/`changeme` for MinIO)
- **Security**: `SECURITY.md` exists with reporting policy, but no secrets scanning, no SBOM, no dependency auditing in CI
- **Community readiness**: `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE` (MIT) all present — signals intent for open collaboration
- **Deployment**: Single-host Docker Compose only — no Kubernetes manifests, no multi-region, no HA

---

## Key Architectural Decisions

1. **Docker Compose single-host deployment** — Simplest operational model for a small team. No Kubernetes overhead. Trade-off: no horizontal scaling, no built-in HA.

2. **SQLite default with Postgres upgrade path** — Zero-config startup for evaluation/development. Postgres recommended for production but not enforced. The schema (`db/schema.sql`) is SQLite-compatible (no Postgres-specific features).

3. **Local-first AI via Ollama** — All LLM inference runs locally (llama3 model). No API keys, no data sent to third parties, no per-token costs. Trade-off: requires GPU or sufficient CPU/RAM.

4. **Telegram as the notification/chat interface** — Ubiquitous, free, mobile-friendly. Webhook-based integration. No need to build a custom mobile app.

5. **Hermes Agent skills for workflow automation** — The 6 skills define the training pipeline as composable, agent-executable workflows. This is the primary integration point with the broader JorahOne ecosystem.

6. **Qdrant for semantic search** — Lightweight, Docker-native vector database. Enables semantic search over training content (transcripts, lessons) without a heavy Elasticsearch stack.

7. **MinIO for video storage** — S3-compatible API means the storage layer can be swapped for AWS S3, GCS, or any S3-compatible backend without code changes.

8. **FastAPI with SQLAlchemy** — Modern async Python stack. Auto-generated OpenAPI docs at `/docs`. SQLAlchemy provides ORM flexibility across SQLite/Postgres.

---

## Repository Structure

```
LearnForge/
├── api/                          # FastAPI backend
│   ├── app.py                    # App entry point (v0.2.0)
│   ├── Dockerfile                # Python 3.11-slim container
│   ├── requirements.txt          # Python dependencies
│   ├── routes/
│   │   └── training.py          # All REST endpoints (users, videos, quizzes, paths, events)
│   └── bots/
│       └── telegram.py           # Telegram webhook handler
├── db/
│   └── schema.sql                # SQLite schema (10 tables)
├── docs/                         # Documentation (several stubs)
│   ├── overview.md               # Stub — 2 lines
│   ├── setup.md                  # Stub — 2 lines
│   ├── deploy.md                 # Production setup guide (complete)
│   ├── observability.md          # Stub — garbled
│   ├── composer-cli.md           # Stub — garbled
│   ├── skill-authors.md          # Partial — skill authoring reference
│   └── reference.md              # Pipeline config reference
├── ops/                          # Operations
│   ├── roadmap.md                # 4-week deployment roadmap
│   └── hermes-wiring.md          # Hermes Agent integration guide
├── scripts/                      # Utility scripts
│   ├── bootstrap.sh              # First-run setup (env + compose up + ollama pull)
│   └── test_api.sh               # Smoke test (health, create user, upload video)
├── skills/                       # Hermes Agent skill definitions (6 skills)
│   ├── training-ingestion/
│   ├── quiz-generator/
│   ├── learning-path-engine/
│   ├── progress-tracker/
│   ├── content-creator/
│   └── telegram-training-bot/
├── .github/workflows/
│   └── ci.yml                    # CI — compose lint only
├── docker-compose.yml            # 4 services + 4 volumes
├── compose.env.example           # Environment variable template
├── Makefile                      # Build automation (bootstrap, up, down, test, deploy, clean)
├── AGENTS.md                     # Stub — garbled 2 lines
├── README.md                     # Primary documentation
├── LICENSE                       # MIT
├── CODE_OF_CONDUCT.md            # Contributor Covenant v2.1
├── CONTRIBUTING.md               # Contribution guide
├── SECURITY.md                   # Security policy (90-day disclosure)
└── .gitignore                    # Ignores .env, media files, cache
```

---

## Notes

- **AGENTS.md is a stub** — Contains only garbled text ("Postgres/OVitalfilesystem -- flagged Hermes Hermes."). This file should either be removed or populated with actual agent configuration.
- **Several docs are stubs** — `docs/overview.md`, `docs/setup.md`, `docs/observability.md`, `docs/composer-cli.md` contain incomplete or garbled placeholder text. Only `docs/deploy.md` and `ops/` files are substantive.
- **No model definitions file** — The `api/app.py` imports model classes (`LearningPath`, `User`, `Video`, `Quiz`, etc.) but these are not defined in the current codebase. They likely live in a missing `models.py` or are generated by SQLAlchemy from the schema. This is a gap — the app would fail to import as-is.
- **CI is minimal** — Only validates Docker Compose syntax. No unit tests, no integration tests, no security scanning, no build verification.
- **No health checks in compose** — Services have `restart: unless-stopped` but no `healthcheck` stanza. Docker has no way to know if the API is actually responding.
- **Default SQLite** — The schema uses SQLite syntax (`INTEGER PRIMARY KEY AUTOINCREMENT`). Switching to Postgres would require schema changes.
- **Git history** — 14 commits. Initial commit created the skeleton. Subsequent commits added routes, skills, docs, and README polish. Recent commits include dependency bumps and a security audit (email sanitization). No branches other than `master`.
- **No test framework** — Only a shell script smoke test (`scripts/test_api.sh`). No pytest, no unit tests, no integration tests.
- **Repo renamed to LearnForge** — Formerly `it-training-system`. All references updated.
