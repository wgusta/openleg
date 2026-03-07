# CLAUDE.md

## Project

OpenLEG: free, open-source public infrastructure for Swiss Lokale Elektrizitätsgemeinschaften (LEG). Municipality-first onboarding (B2G), resident registration and matching (B2C), free public energy data API. Flask + PostgreSQL + OpenClaw AI.

Tagline: Freie Infrastruktur für Schweizer Stromgemeinschaften.

Mission: Maximize the number of functioning LEGs in Switzerland. Maximize their autarky. Minimize their costs. Never sell citizen data.

## Swiss German Text Rules

All user-facing German text MUST use proper Schweizer Hochdeutsch:
- Always use real umlauts: ä, ö, ü (NEVER ae, oe, ue as substitutes)
- Always use ss instead of ß (Swiss standard: Strasse not Straße, heisst not heißt)
- Active voice (Aktiv), never passive (Passiv)
- No em dashes, en dashes. Use commas, colons, semicolons.
- URLs and code identifiers keep ASCII (e.g. `/leg-gruenden`, `fuer_bewohner.html`)

## Architecture

Runs on Infomaniak VPS (83.228.223.66) via Docker Compose:
- **flask**: gunicorn on :5000, Python 3.11
- **postgres**: PostgreSQL 16, volume `postgres_data`
- **openclaw**: AI gateway on :18789 with MCP server (DB access), autonomous LEG enablement agent
- **caddy**: reverse proxy, auto TLS

Domains: `openleg.ch` (Flask), `<city>.openleg.ch` (multi-tenant municipalities), `api.openleg.ch` (Public API), `claw.openleg.ch` (OpenClaw)

Repo: `github.com/wgusta/openleg`

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Flask app, all routes |
| `database.py` | PostgreSQL layer, 23+ tables, all CRUD |
| `public_data.py` | ElCom SPARQL, Energie Reporter, Sonnendach fetchers + computed metrics |
| `api_public.py` | Public REST API Blueprint (`/api/v1/*`), no auth, CORS |
| `health.py` | Health check blueprint: `/health`, `/livez` |
| `tenant.py` | Multi-tenant resolution: `<city>.openleg.ch` |
| `municipality.py` | Municipality onboarding + profil/verzeichnis pages |
| `meter_data.py` | Smart meter CSV parsing (EKZ, ewz, CKW, BKW formats) |
| `insights_engine.py` | Compute: load profiles, solar index, flexibility (for LEG members, not sold) |
| `formation_wizard.py` | LEG formation flow, financial model, business case |
| `ml_models.py` | DBSCAN clustering |
| `email_automation.py` | SMTP drip campaigns |
| `security_utils.py` | Input validation, sanitization |
| `data_enricher.py` | Geocoding (Swisstopo), energy profiles (BFE Sonnendach) |
| `stripe_integration.py` | Dormant, kept for optionality |
| `templates/pilotgemeinde_baden.html` | Baden pilot case study (real ElCom + Sonnendach data, BFS 4021) |

## Deploy

```bash
# Full deploy: tests -> rsync -> build -> verify
bash deploy.sh

# Manual (on VPS)
ssh -i ~/.ssh/infomaniak_badenleg ubuntu@83.228.223.66
cd /opt/badenleg && docker compose up -d --build flask
```

## Dev

```bash
# Local dev (needs .env with DATABASE_URL pointing to a Postgres instance)
python app.py  # runs on :5003

# Run tests
pytest tests/ -v
```

## Environment

All env vars in `.env` on VPS. See `.env.example`. `DATABASE_URL` set automatically in docker-compose.yml for flask and openclaw services.

## Admin

`/admin/overview` requires `ADMIN_TOKEN` header.

## Public API

`/api/v1/*` endpoints are open, no auth required. Rate limited 60/min per IP. CORS enabled. Docs at `/api/v1/docs`.

Key endpoints:
- `GET /api/v1/municipalities` - List with profiles
- `GET /api/v1/municipalities/<bfs>/tariffs` - ElCom tariffs
- `GET /api/v1/municipalities/<bfs>/leg-potential` - Value-gap analysis
- `POST /api/v1/leg/financial-model` - 10-year projections
- `GET /api/v1/rankings` - Ranked municipalities

## Cron

- `POST /api/cron/refresh-public-data` (X-Cron-Secret) - Refresh ElCom + Energie Reporter + Sonnendach
- `POST /api/cron/process-emails` (X-Cron-Secret) - Process email queue
- `POST /api/cron/process-billing` (X-Cron-Secret) - Run billing for active communities
- `GET /metrics` - Platform metrics (active_communities, total_buildings)

## Data Sources (public, no PII)

| Source | Data | Update |
|--------|------|--------|
| ElCom (LINDAS SPARQL) | Electricity tariffs per operator/municipality | Yearly |
| BFE Sonnendach (opendata.swiss) | Solar potential per municipality | Periodic |
| Energie Reporter (opendata.swiss) | Solar, EV, heating, consumption per municipality | Quarterly |
| Swisstopo (api3.geo.admin.ch) | Address geocoding, PLZ | Real-time |

## OpenClaw Operations

`claw.openleg.ch` runs the OpenClaw AI gateway. New browser sessions require device pairing approval.

**If "pairing required" error appears:**
```bash
ssh -i ~/.ssh/infomaniak_badenleg ubuntu@83.228.223.66
cd /opt/badenleg
docker compose exec openclaw openclaw devices list    # find pending request ID
docker compose exec openclaw openclaw devices approve <requestId>
```

**If "password_missing" / "unauthorized" error:** gateway password is `OPENCLAW_GATEWAY_PASSWORD` in `.env`. Enter it in the Control UI settings panel.

**Restart OpenClaw:** `cd /opt/badenleg && docker compose up -d --build openclaw`

## Data Policy

Citizen smart meter data stays within their LEG. Never sold, never aggregated for third parties. Insights engine outputs serve LEG members only.

## Development Workflow

Every change follows a pipeline. Skip stages when scope is small.

```
Idea → Research → Prototype → PRD → Kanban → Execution → QA
```

### 1. Idea
As small or as big as needed. Bug report, feature idea, strategic initiative.

### 2. Research
Put all findings into `research.md`. Reference stale entries. Check freshness dates before trusting existing research.

### 3. Prototype
Use sub-agents in parallel to visualize 2-3 different approaches. Use `/deepening` or `/design-an-interface` skills. Never implement the first idea.

### 4. PRD
Create `prd/<feature>.md` with acceptance criteria. No implementation without acceptance criteria. See `SKILLS.md` for `/prd-write`.

### 5. Kanban
Create GitHub issues from PRD acceptance criteria. Use labels: `p0`/`p1`/`p2`, `seo`, `infrastructure`, `strategic`, `research`, `grant`, `academic`, `discipline`.

### 6. Execution
- **Sequential:** Ralph Loop for focused single-task execution
- **Parallel:** `git worktree` for independent tasks (Agent with `isolation: "worktree"`)
- **Human-in-the-loop:** `AskUserQuestion` at decision points

### 7. QA
TDD: write failing test first, implement, refactor. Run `pytest tests/ -v`. Delegate code review to Codex CLI. Iterate through 5-6-7 until done.

### Shortcuts
- Bug fix: `/tdd → review`
- SEO work: `/research → execute → review`
- Infrastructure: `/kanban → execute → tdd`

## Feature Discipline

**No new features until 3 municipalities have active registrations.**

Allowed: bug fixes, SEO/content, CI/infra, grants, academic outreach, docs.

Decision filter: "Does this help a citizen discover or form a LEG?"
- Yes directly (SEO, onboarding fix): do it now
- Yes indirectly (CI, docs, grants): do it this week
- No (new billing feature, new API, new ML model): skip

See `prd/feature-discipline.md` for full policy and deferred features list.

## Project Docs

| File | Purpose |
|------|---------|
| `research.md` | Living research document (competitive, regulatory, market, SEO) |
| `seo-strategy.md` | Content/SEO strategy with phased implementation |
| `prd/github-bfe-academic.md` | PRD: GitHub hardening, BFE grants, academic partnerships |
| `prd/feature-discipline.md` | PRD: Feature freeze policy and deferred items |
| `SKILLS.md` | Development workflow skills and their triggers |
| `PIVOT.md` | Active strategy (replaces B2B model from open-strategy.md) |
| `FUTURE.md` | Deferred strategic items with preconditions |
| `open-strategy.md` | Pre-pivot B2B strategy (regulatory + competitive sections still canonical) |
