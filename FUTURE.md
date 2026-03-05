# FUTURE.md

Deferred strategy items. Revisit when preconditions met.

## 1. GitHub Public + AGPL-3.0

Repo is PUBLIC at github.com/wgusta/openleg. CI has tests, secret scan, forbidden paths.

Remaining hardening (tracked in `prd/github-bfe-academic.md` and GitHub issues #4-#9):
- [ ] Ruff lint + format check (#4)
- [ ] Mypy type check (#5)
- [ ] AGPL license headers (#6)
- [ ] CONTRIBUTING.md update (#7)
- [ ] Issue templates (#8)
- [ ] Dependabot (#9)

**Status:** In progress. No longer blocked.

## 2. Self-hosting Documentation

`deploy.example.sh` exists. Needs:
- Step-by-step guide for VPS setup (Caddy, Postgres, Docker Compose)
- `.env.example` with all vars documented
- One-click DigitalOcean/Hetzner deploy button
- Upgrade path documentation

**Precondition:** AGPL public release done.

## 3. SDAT-CH Integration

Standardized Swiss data exchange for metering (SDAT-CH/eCH-0218). Long-term moat:
- Automated meter data exchange with VNBs
- Real-time 15-min interval data instead of monthly CSV
- Eliminates manual smart meter uploads

**Precondition:** Post-funding, partnership with at least 1 VNB.
