# Dashboards V2 Robust Adaptation

## Summary
- Goal: portable dashboard modules with explicit admin privacy invariants.
- Branch/worktree model: independent `codex/*` branches from `origin/main`.
- No public route removals in this pass.
- Keep `/admin/pipeline` active and protected.

## Branches
1. `codex/dashboards-v2-0-admin-guard`
2. `codex/dashboards-v2-1-gemeinde-foundation`
3. `codex/dashboards-v2-2-utility`
4. `codex/dashboards-v2-3-resident-blueprint`
5. `codex/dashboards-v2-4-admin-blueprint`

## PR0: Admin Guard
- Add admin privacy guard tests for:
  - `/admin/overview`
  - `/admin/pipeline`
  - `/admin/export`
  - `/admin/lea-reports`
  - `/api/email/stats`
  - `/api/billing/community/<community_id>/period/<period_id>`
- Enforce header-only admin auth (`X-Admin-Token`) in app/admin surfaces.
- Keep fail-closed behavior when `ADMIN_TOKEN` missing (`404`).

## PR1: Foundation + Gemeinde
- Add shared dashboard partials:
  - `templates/partials/dashboard_head.html`
  - `templates/partials/dashboard_nav.html`
- Migrate `templates/gemeinde/dashboard.html` to shared partials.
- Ensure noindex robots meta through shared head.
- Keep `subdomain`/`bfs` query behavior.
- Pass `ga4_id` explicitly in municipality dashboard route.
- Add Gemeinde dashboard tests for routing + rendering invariants.

## PR2: Utility
- Migrate `templates/utility/dashboard.html` to shared partials.
- Keep auth flow unchanged (`/utility/dashboard` requires session).
- Remove stale onboarding copy: `White-Label Branding konfigurieren`.
- Add first direct utility dashboard tests (auth redirect + UI invariants).

## PR3: Resident Blueprint
- Extract resident routes from `app.py` into `resident_dashboard.py`:
  - `/dashboard`
  - `/api/referral/stats/<building_id>`
  - `/api/referral/leaderboard`
- Register blueprint in app.
- Preserve route paths and behavior.
- Add parity tests for readiness score, referral link, noindex, leaderboard behavior.

## PR4: Admin Blueprint
- Extract admin routes from `app.py` into `admin_dashboard.py`:
  - `/admin/overview`
  - `/admin/pipeline`
  - `/admin/export`
  - `/admin/lea-reports`
- Register blueprint in app.
- Keep `/admin/pipeline` available and protected.
- Add admin dashboard tests for auth and response contracts.

## Test Protocol
- Per PR: run impacted tests first.
- Then run broader suite (`pytest tests/ -v`) before merge when infra allows.
- Mandatory gate: no unauthenticated `200` on admin surfaces.

## Acceptance Criteria
- Admin dashboard surfaces are not public.
- Dashboard shells are portable via shared partials.
- Route contracts remain stable per PR scope.
- No broad B2B archival in this pass.
