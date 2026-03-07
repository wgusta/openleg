# PRD: Feature Discipline

**Status:** Active (permanent policy)
**Priority:** P0

---

## Context

OpenLEG has 37 DB tables, 62 test files, 42 templates, 16+ API endpoints, and zero active users. The platform is overbuilt. Every hour of new feature development has negative ROI until distribution catches up.

## The Rule

**No new features until 3 municipalities have active resident registrations.**

Exceptions (things that ARE allowed):
- Bug fixes on existing features
- SEO/content work (drives distribution)
- CI/infrastructure hardening (enables collaboration)
- Grant applications (funds operations)
- Academic outreach (drives API usage)
- Documentation (enables self-service)

## Decision Filter (Post-Pivot)

Before writing any code, ask: **"Does this help a citizen discover or form a LEG?"**

- **Yes, directly** (SEO, content, onboarding fix): do it now
- **Yes, indirectly** (CI, docs, grants): do it this week
- **No** (new billing feature, new API endpoint, new ML model): skip it
- **Maybe**: check if a municipality or resident requested it

## What Gets Deferred

| Feature | Why Deferred | Revisit When |
|---------|-------------|--------------|
| `stripe_integration.py` | Dormant since pivot, no revenue model needs it | Revenue model requires payments |
| SDAT-CH integration | 2-3 months engineering, needs VNB partnership | Post-funding, 1+ VNB partner |
| FR/IT translations | No Romandie users yet | First Romandie municipality registers |
| Redis caching | In-memory cache sufficient at current scale | 50+ concurrent tenants |
| E-signature (DeepSign) | Already wired, but no formations to sign | First real LEG formation |
| Webhook delivery system | No external integrations requesting it | First API client asks |
| Partner APIs (solar installers) | No partners yet | First partnership signed |
| ML load forecasting | No meter data to forecast | 10+ buildings with meter uploads |

## Cleanup Candidates

| Item | Action | Priority |
|------|--------|----------|
| `stripe_integration.py` | Keep file, add deprecation comment | P2 |
| `utility_portal.py` | Audit: is it wired post-pivot? | P2 |
| `open-strategy.md` B2B sections | Mark stale, add header warning | P1 |
| Unused DB tables | Audit which tables have zero rows in prod | P2 |

## Acceptance Criteria

- [x] **FD-1**: CLAUDE.md updated with feature discipline section ✅ 2026-03-05
- [ ] **FD-2**: `open-strategy.md` gets a stale warning header
- [ ] **FD-3**: GitHub issue template `feature-request.md` includes the decision filter
- [ ] **FD-4**: No PRD created for new features until 3 active municipalities

---

## How This Changes

When the gate is met (3 municipalities with active registrations), revisit `FUTURE.md` and this document. The priority shifts from distribution to retention and feature depth.
