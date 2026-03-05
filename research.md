# Research

Living document. All market, regulatory, competitive, and technical research for OpenLEG. Referenced by PRDs and decision-making.

## Freshness Index

| Topic | Last Updated | Status | Source |
|-------|-------------|--------|--------|
| Regulatory (StromVG/StromVV) | 2026-02-24 | Fresh | `open-strategy.md` |
| Competitive landscape | 2026-02-24 | Needs refresh | `open-strategy.md` |
| Market sizing (631 DSOs) | 2026-02-24 | Fresh | `open-strategy.md` |
| ElCom tariff data | 2026-03-05 | Fresh | Auto-refresh via cron |
| Energie Reporter | 2026-03-05 | Fresh | Auto-refresh via cron |
| BFE Sonnendach | 2026-03-05 | Fresh | Auto-refresh via cron |
| SEO/content landscape | 2026-03-05 | New | `seo-strategy.md` |
| BFE grant programs | — | Not started | — |
| Academic partnerships | — | Not started | — |

---

## Regulatory Framework

Source: `open-strategy.md` "What the Law Actually Says"

- **LEG law:** Art. 17d/17e StromVG, Art. 19e-19h StromVV
- **Effective:** 2026-01-01 (Mantelerlass)
- **Network discount:** 40% same level, 20% cross-level
- **Metering:** 15-min intervals mandatory
- **Smart meters:** DSO must install within 3 months of request
- **Agreement:** Written internal agreement required (Art. 17e)
- **Scope:** Federal law, no cantonal variation for LEG formation
- **SDAT-CH:** New 2025 edition goes live 2026-03-24

**Still valid.** No changes expected for years.

---

## Competitive Landscape

Source: `open-strategy.md` "The Competitive Landscape". Last verified: 2026-02-24.

| Player | Focus | Threat | Status |
|--------|-------|--------|--------|
| LEGHub (Swisspower/Ajila/jls) | Top 22 utilities, ERP-dependent | Medium | 4 live clients. Requires ERP integration (SAP/InnoSolv/ESL-EVU). 3-year lock-in. |
| OWT (Lausanne) | Romandie LECs | Low (DE market) | French-speaking focus, free for LEC admins |
| smart-me (Zug) | Hardware + software | Low | Sells meter hardware bundles, not pure SaaS |
| Softcom Technologies (Fribourg) | Energy Hub, digital twin | Low | Still building LEC features, 80 employees |
| enshift / lokalerstrom.ch | LEG/vZEV/ZEV tools | Low | Small market presence |
| **"Do nothing / Excel"** | Status quo | **HIGH** | Real competitor for small DSOs with 0-2 LEG requests |

**STALE CHECK NEEDED:** LEGHub client count (last verified Feb 2026). Monitor `leghub.ch` monthly.

### SEO Competitors

See `seo-strategy.md` for detailed content gap analysis.

---

## Market Sizing

- 631 DSOs in Switzerland
- ~600 electricity utilities
- 4 on LEGHub, 627 unserved
- 2,131 municipalities total
- Median household electricity price: 27.7 Rp/kWh (2026)
- LEG value gap: 2-6 Rp/kWh per household
- CHF 90-270/year savings per household (4,500 kWh basis)

---

## Data Sources (Public, No Auth)

| Source | Endpoint | Format | Refresh |
|--------|----------|--------|---------|
| ElCom tariffs | LINDAS SPARQL | RDF | Cron (yearly data) |
| BFE Sonnendach | opendata.swiss | CSV/JSON | Cron (periodic) |
| Energie Reporter | opendata.swiss | JSON | Cron (quarterly) |
| Swisstopo geocoding | api3.geo.admin.ch | REST/JSON | Real-time |

---

## BFE Grant Programs

**Status: NOT STARTED. High priority.**

Research needed:
- [ ] BFE Pilot & Demonstration programs: current call status, eligibility for digital infrastructure
- [ ] EnergieSchweiz: alignment with "Energieeffizienz" or "Erneuerbare Energien" programs
- [ ] Cantonal energy office digitalization budgets (focus: ZH, AG, BE)
- [ ] Pronovo: renewable energy support eligibility for LEG platform
- [ ] Foundation grants: Mercator Schweiz, Ernst Göhner Stiftung, Engagement Migros
- [ ] Innosuisse Innovation Cheque (CHF 15K for university collaboration)
- [ ] Climate-KIC / EIT InnoEnergy Swiss chapter

**Target:** CHF 50K covers 8+ years of infrastructure costs (CHF 500/mo VPS).

---

## Academic Partnerships

**Status: NOT STARTED. Medium priority.**

Research needed:
- [ ] ETH Energy Science Center: student thesis using OpenLEG API/data
- [ ] ZHAW School of Engineering: energy informatics program, project work
- [ ] HSLU: energy management studies, semester projects
- [ ] FHNW: renewable energy program collaboration
- [ ] Uni Bern / Uni Zürich: energy law clinics (legal validation)
- [ ] Innosuisse: co-funding model with academic partner

**Value:** Academic users create API traffic, contribute data quality checks, publish papers citing OpenLEG. Low-cost distribution channel.

---

## Pivot History

| Date | Event |
|------|-------|
| Pre-2026 | B2B SaaS targeting EVUs (CHF 500-9900/mo) |
| 2026-01-01 | Mantelerlass takes effect |
| 2026-02-24 | `open-strategy.md`: 12-week B2B execution plan |
| 2026-02-25 | `PIVOT.md`: Pivot to free public infrastructure |

**Pivot rationale:** B2B revenue model had <35% success probability. Selling citizen data contradicts autonomy mission. Free removes price objection. Infrastructure costs CHF 500/mo, funded personally or via grants.

**`open-strategy.md` status:** Revenue model, sales process, and org structure sections are STALE (pre-pivot). Regulatory framework, competitive landscape, and data source sections remain CANONICAL references.
