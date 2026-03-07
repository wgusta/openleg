# PRD: GitHub Hardening, BFE Grant, Academic Partnerships

**Status:** Draft
**Priority:** P0 (unblocks everything else)
**Branch:** `feat/github-hardening`

---

## Context

Repo is public at `github.com/wgusta/openleg`. CI has test runner, secret scan, forbidden paths. But no lint, no type check, no license headers, no CONTRIBUTING.md update, no GitHub Issues as project management. BFE grant and academic partnerships not started.

## Goals

1. Make GitHub repo credible for grants, academics, contributors
2. Submit BFE grant application
3. Initiate 2-3 academic partnerships
4. Establish GitHub Issues as the project kanban

---

## Acceptance Criteria

### GitHub Hardening

- [ ] **GH-1**: CI workflow adds `ruff` lint + `ruff format --check` (fail on violations)
- [ ] **GH-2**: CI workflow adds `mypy --ignore-missing-imports` on core files (app.py, database.py, api_public.py, formation_wizard.py)
- [ ] **GH-3**: License header check: all `.py` files start with `# SPDX-License-Identifier: AGPL-3.0-or-later`
- [ ] **GH-4**: `LICENSE` file is AGPL-3.0 (verify present and correct)
- [ ] **GH-5**: `CONTRIBUTING.md` updated for post-pivot (free platform, not B2B SaaS)
- [ ] **GH-6**: GitHub Issue templates: `bug.md`, `feature-request.md`, `research.md`
- [ ] **GH-7**: GitHub project board created (kanban: Backlog, Ready, In Progress, Review, Done)
- [x] **GH-8**: Labels created: `strategic`, `seo`, `infrastructure`, `research`, `grant`, `academic`, `p0`, `p1`, `p2` ✅ 2026-03-05
- [ ] **GH-9**: Dependabot enabled for pip dependencies
- [ ] **GH-10**: Branch protection on `main`: require PR, require CI pass

### BFE Grant

- [ ] **BFE-1**: Research all active BFE funding programs (Pilot, Demo, EnergieSchweiz). Document in `research.md`
- [ ] **BFE-2**: Research cantonal energy office digitalization budgets (ZH, AG, BE)
- [ ] **BFE-3**: Draft grant application (project description, budget, timeline, impact metrics)
- [ ] **BFE-4**: Identify 2 foundation grants (Mercator, Ernst Göhner, Engagement Migros) and check eligibility
- [ ] **BFE-5**: Submit first application

### Academic Partnerships

- [ ] **AC-1**: Research ETH Energy Science Center thesis program. Find contact person.
- [ ] **AC-2**: Research ZHAW energy informatics. Find contact person.
- [ ] **AC-3**: Research Innosuisse Innovation Cheque (CHF 15K). Check eligibility with academic partner.
- [ ] **AC-4**: Draft 1-page partnership proposal (what OpenLEG offers: API, data, real platform; what we need: thesis students, data validation, publications)
- [ ] **AC-5**: Send first outreach email to 2 institutions

---

## Implementation Plan

### Phase 1: GitHub Hardening (1-2 days)

1. Add `ruff` to `requirements-dev.txt`, create `ruff.toml` config
2. Add lint + type check CI workflow
3. Add license header check script + CI step
4. Create issue templates in `.github/ISSUE_TEMPLATE/`
5. Create GitHub labels via `gh label create`
6. Enable Dependabot (`dependabot.yml`)
7. Set branch protection rules

### Phase 2: BFE Grant Research (3-5 days)

1. Web research on all BFE programs
2. Document findings in `research.md`
3. Draft application
4. Review with advisor/mentor if available

### Phase 3: Academic Outreach (1-2 weeks)

1. Identify contacts at ETH, ZHAW
2. Draft partnership proposal
3. Send outreach
4. Follow up

---

## Risks

| Risk | Mitigation |
|------|-----------|
| Ruff lint finds hundreds of violations | Fix incrementally, start with `--select E,W` (errors+warnings only) |
| BFE programs not open for digital infrastructure | Pivot to cantonal programs or foundations |
| Academics not interested | Lower the ask: offer data access for existing research, not dedicated thesis |

---

## Success Metrics

| Metric | Target | Timeline |
|--------|--------|----------|
| CI checks passing | 100% | Week 1 |
| GitHub issues created | 20+ | Week 1 |
| Grant applications submitted | 1 | Month 1 |
| Academic contacts made | 3 | Month 1 |
| First academic user on API | 1 | Month 3 |
