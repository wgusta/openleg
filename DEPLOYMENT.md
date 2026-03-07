# Deployment Guide

## Infrastructure

Infomaniak VPS (83.228.223.66), Docker Compose, Caddy with auto TLS.

SSH: `ssh -i ~/.ssh/infomaniak_openleg ubuntu@83.228.223.66`

## Services

| Service | Image | Port | Domain |
|---------|-------|------|--------|
| flask | Custom (Python 3.11) | 5000 | openleg.ch |
| postgres | postgres:16-alpine | 5432 | internal |
| openclaw | Custom (Node) | 18789 | openclaw.openleg.ch |
| caddy | caddy:latest | 80, 443 | reverse proxy |

## Deploy Changes

```bash
# Sync files to VPS
rsync -avz --exclude='.git' --exclude='.env' --exclude='__pycache__' \
  -e "ssh -i ~/.ssh/infomaniak_openleg" \
  ./ \
  ubuntu@83.228.223.66:/opt/openleg/

# Rebuild and restart
ssh -i ~/.ssh/infomaniak_openleg ubuntu@83.228.223.66 \
  "cd /opt/openleg && docker compose up -d --build"
```

To rebuild only flask: `docker compose up -d --build flask`

## First Time Setup

1. Provision VPS, install Docker
2. Create `/opt/openleg/` directory
3. rsync project files
4. Create `.env` from `.env.example` with real secrets
5. `docker compose up -d`
6. Verify: `curl https://openleg.ch`

## Database

PostgreSQL 16, data in Docker volume `postgres_data`.

Tables auto-created by `database.py:init_db()` on first Flask boot.

### Backup

```bash
ssh -i ~/.ssh/infomaniak_openleg ubuntu@83.228.223.66 \
  "docker exec openleg-postgres pg_dump -U badenleg badenleg" > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
cat backup.sql | ssh -i ~/.ssh/infomaniak_openleg ubuntu@83.228.223.66 \
  "docker exec -i openleg-postgres psql -U badenleg badenleg"
```

## DNS

A records pointing to 83.228.223.66:
- `openleg.ch` (A record)
- `*` wildcard (A record)
- `www` (CNAME to openleg.ch)

Caddy handles TLS certificates automatically.

## Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f flask
docker compose logs -f postgres
```

## Troubleshooting

```bash
# Check container health
docker compose ps

# Restart all
docker compose restart

# Rebuild from scratch
docker compose down && docker compose up -d --build

# Check postgres connectivity
docker exec openleg-postgres pg_isready -U badenleg
```

## Verification Checklist

- [ ] `curl https://openleg.ch` returns landing page
- [ ] `curl https://openclaw.openleg.ch` returns WebChat UI
- [ ] `/admin/overview` works with ADMIN_TOKEN
- [ ] Address autocomplete works
- [ ] Registration flow completes
- [ ] Email confirmation sends
- [ ] Caddy logs show TLS certs issued
