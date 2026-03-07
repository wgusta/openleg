# Portable Dashboards Plan

## Context
4 dashboards exist but are not portable: no template inheritance, inconsistent patterns, stale B2B artifacts, weak test coverage. Goal: make each dashboard a clean, self-contained, open-source-ready module with TDD. Sequential execution so learnings transfer forward.

## Branch Strategy
4 branches off `main`, 4 separate PRs. Each PR is independently reviewable.

| Order | Branch | Dashboard | Rationale |
|-------|--------|-----------|-----------|
| 1 | `dashboards/1-gemeinde` | Gemeinde | Simplest (98-line template, already blueprinted, 7 existing tests). Establishes shared patterns. |
| 2 | `dashboards/2-utility` | Utility | Already blueprinted, 162-line template, zero tests. Apply patterns from #1. |
| 3 | `dashboards/3-resident` | Resident | Inline in app.py, needs blueprint extraction. Apply patterns from #1+#2. |
| 4 | `dashboards/4-admin` | Admin | Most complex, stale VNB removal, blueprint extraction. All patterns proven by now. |

## Shared Infrastructure (established in PR 1, reused in 2-4)

### New partials
- `templates/partials/dashboard_head.html`: charset, viewport, tailwind_brand include, noindex, favicon, conditional GA4
- `templates/partials/dashboard_nav.html`: minimal nav with `{{ dashboard_title }}`, optional `{{ back_url }}`, optional `{{ logout_url }}`

### Test pattern
Reusable pattern using `patch.object(app_module.db, 'func_name')` (not `patch('database.func_name')`) to avoid the stale MagicMock gotcha.

## PR 1: Gemeinde Dashboard

**Branch:** `dashboards/1-gemeinde` from `main`

**Changes:**
- Create `templates/partials/dashboard_head.html` + `dashboard_nav.html`
- Fix `templates/gemeinde/dashboard.html`: replace HTML entities (`&uuml;` -> `ü`) with real UTF-8 umlauts
- Adopt shared partials in template
- Pass `ga4_id` from route in `municipality.py:347`

**TDD tests** (`tests/test_gemeinde_dashboard.py`):
1. `test_dashboard_umlauts` - real `ü`/`ä`, no `&uuml;`
2. `test_dashboard_includes_nav` - shared nav present
3. `test_dashboard_noindex` - robots noindex meta
4. `test_dashboard_bfs_lookup` - access via `?bfs=261`
5. `test_dashboard_formation_button_threshold` - button at 3+, hidden below
6. `test_dashboard_invite_link` - correct invite URL

**Transfer to PR 2:** Shared partials exist. Dashboard test pattern established.

## PR 2: Utility Dashboard

**Branch:** `dashboards/2-utility` from `main`

**Changes:**
- Adopt shared partials in `templates/utility/dashboard.html`
- Remove stale B2B onboarding text ("White-Label Branding")
- Add noindex meta
- Verify Swiss German text consistency

**TDD tests** (`tests/test_utility_dashboard.py`):
1. `test_dashboard_requires_auth` - unauthenticated redirects to login
2. `test_dashboard_renders_client_data` - shows company_name
3. `test_dashboard_noindex` - robots noindex
4. `test_dashboard_status_badges` - correct badge for active/trial
5. `test_dashboard_api_key_section` - API key UI present
6. `test_dashboard_onboarding_steps` - checklist renders

**Transfer to PR 3:** Session auth test pattern proven. Template cleanup patterns refined.

## PR 3: Resident Dashboard

**Branch:** `dashboards/3-resident` from `main`

**Changes:**
- Extract from `app.py` to new `resident_dashboard.py` Blueprint:
  - `_require_dashboard_token()` (~10 lines)
  - `/dashboard` route (~50 lines)
  - `/api/referral/stats` + `/api/referral/leaderboard` routes
- Register blueprint in `app.py`
- Adopt shared partials in `templates/dashboard.html`

**TDD tests** (`tests/test_resident_dashboard.py`):
1. `test_no_token_403` - 403 without token
2. `test_invalid_token_403` - 403 with bad token
3. `test_valid_token_renders` - shows readiness score
4. `test_readiness_score_100` - all 4 checks = 100%
5. `test_readiness_score_partial` - 2 checks = 50%
6. `test_neighbor_count` - displays neighbor count
7. `test_referral_link` - displays referral link
8. `test_noindex` - robots noindex
9. `test_savings_form_present` - savings calculator form exists

**Transfer to PR 4:** Blueprint extraction pattern proven (extract from app.py, register, update imports).

## PR 4: Admin Dashboard

**Branch:** `dashboards/4-admin` from `main`

**Changes:**
- Extract from `app.py` to new `admin_dashboard.py` Blueprint:
  - `_require_admin()` (~7 lines)
  - `/admin/overview`, `/admin/strategy`, `/admin/export`, `/admin/lea-reports` routes
- **Archive stale VNB pipeline:**
  - Remove `/admin/pipeline` route from app
  - Move `sales_pipeline.py` -> `archived/sales_pipeline.py`
  - Move `templates/admin/pipeline.html` -> `archived/templates/pipeline.html`
  - Move `tests/test_admin_pipeline.py` -> `archived/tests/test_admin_pipeline.py`
- Fix English text in `strategy.html`: "Stuck Communities" -> "Blockierte Gemeinschaften", etc.
- Adopt shared partials in `templates/admin/strategy.html`

**TDD tests** (`tests/test_admin_dashboard.py`):
1. `test_overview_requires_token` - 403 without token
2. `test_overview_returns_stats` - JSON with platform stats
3. `test_strategy_requires_token` - 403 without token
4. `test_strategy_json` - JSON by default
5. `test_strategy_html` - HTML with Accept header
6. `test_strategy_german_text` - German labels, no English
7. `test_export_json` - JSON records
8. `test_export_csv` - CSV with Content-Disposition
9. `test_lea_reports_requires_token` - 403 without token
10. `test_lea_reports_returns_list` - report list
11. `test_pipeline_route_removed` - `/admin/pipeline` returns 404 (archived)

## Portability Checklist (all 4)
- [ ] Self-contained Blueprint
- [ ] Shared partials (dashboard_head, dashboard_nav)
- [ ] No hardcoded URLs (`url_for()`, `site_url`)
- [ ] GA4 via env var (not hardcoded)
- [ ] `noindex, nofollow` meta
- [ ] Real UTF-8 umlauts
- [ ] Active voice German
- [ ] Comprehensive test suite

## Execution Method
Each dashboard: agent in worktree isolation, TDD (write failing tests first, implement, verify green). After tests pass, create branch, commit, push, PR via `gh pr create`.

## Key Files
| File | Role |
|------|------|
| `app.py` | Extract resident (L1629-1679) + admin (L878-970) routes |
| `municipality.py` | Gemeinde dashboard (L330-347) |
| `utility_portal.py` | Utility dashboard (L175-179) |
| `database.py` | All dashboard queries |
| `templates/gemeinde/dashboard.html` | Gemeinde template (98L) |
| `templates/utility/dashboard.html` | Utility template (162L) |
| `templates/dashboard.html` | Resident template (167L) |
| `templates/admin/strategy.html` | Admin strategy template (82L) |
| `templates/admin/pipeline.html` | ARCHIVE (stale B2B) |
| `sales_pipeline.py` | ARCHIVE (stale B2B) |
| `tests/conftest.py` | Test fixtures, mock_db pattern |

## Verification
After each PR:
1. `pytest tests/ -v` all green
2. `python app.py` starts without errors
3. Each dashboard route returns 200 (or correct auth error)
4. Templates render with real umlauts, shared nav, noindex
