# SEO & Content Strategy

**Status:** Active
**Last Updated:** 2026-03-07
**Goal:** Own Swiss LEG search landscape. Zero paid ads. Compound organic traffic through 2131 municipality pages + targeted content.

---

## Current State

### What's Working
- Meta descriptions on all main pages (fuer-bewohner, fuer-gemeinden, index)
- FAQPage schema (7 Q&A pairs) on fuer-bewohner.html (good for featured snippets)
- Dynamic sitemap.xml with all 2131 municipality profile URLs
- robots.txt correctly configured
- Keyword targeting on landing pages: "LEG Gemeinde", "Stromgemeinschaft Schweiz", "StromVG Art 17d"

### What's Missing
- ~~**Canonical tags** on municipality profiles~~ ✅ Done
- ~~**Structured data** on profiles~~ ✅ LocalPlace + BreadcrumbList added
- ~~**og:image** on most pages~~ ✅ Added to profil + verzeichnis
- ~~**Verzeichnis page** has NO meta tags, NO structured data~~ ✅ CollectionPage + canonical added
- ~~**No formation guide page**~~ ✅ `/leg-gruenden` live
- **No canton landing pages** (missing "/leg/zuerich", "/leg/bern" etc.)
- ~~**No financial calculator page**~~ ✅ `/leg-kalkulator` live
- ~~**No case study / pilot page**~~ ✅ `/pilotgemeinde/baden` live (real ElCom + Sonnendach data for BFS 4021)
- **No API developer landing page**
- ~~**H1 tags** on profiles are generic~~ ✅ Keyword-optimized with tariff data
- **Google Search Console** status unknown

---

## The Moat: 2131 Municipality Pages

OpenLEG's biggest SEO asset is 2131 individual municipality profile pages, each containing real ElCom tariff data, solar potential, and LEG value-gap analysis. Competitors have nothing like this.

**Current:** `/gemeinde/profil/{bfs}` exists for every Swiss municipality. Included in sitemap. But not optimized.

**Target:** Each page ranks for "[Gemeinde] Stromtarif 2026" queries. With proper schema, canonical tags, and keyword-optimized H1s, these pages capture thousands of long-tail queries with near-zero competition.

**Why it works:** Nobody else has automated, municipality-specific tariff data pages. LEGHub is B2B only, no public profiles. ElCom data is public but not presented per-municipality in a user-friendly way.

---

## Keyword Strategy

### Tier 1: Own These (High Priority, Achievable)

| Keyword Cluster | Target Page | Monthly Search (est.) | Competition |
|----------------|-------------|----------------------|-------------|
| "[Gemeinde] Stromtarif" x 2131 | /gemeinde/profil/{bfs} | 10-200 each | Near zero |
| "Stromgemeinschaft Schweiz" | /fuer-bewohner | 200-500 | Low |
| "LEG Schweiz" | / (index) | 100-300 | Low |
| "Lokale Elektrizitätsgemeinschaft gründen" | /leg-gruenden (new) | 100-300 | Low |
| "Netzgebühren sparen Gemeinde" | /fuer-gemeinden | 50-150 | Low |

### Tier 2: Build Toward (Medium Priority)

| Keyword Cluster | Target Page | Monthly Search (est.) | Competition |
|----------------|-------------|----------------------|-------------|
| "LEG [Kanton]" (per canton) | /leg/{kanton} (new) | 20-100 each | Zero |
| "Art 17d StromVG LEG" | /fuer-bewohner | 50-100 | Low |
| "LEG Kostenersparnis berechnen" | /leg-kalkulator (new) | 50-100 | Zero |
| "Mantelerlass Stromgemeinschaft 2026" | /leg-gruenden (new) | 30-80 | Zero |

### Tier 3: Authority Building (Lower Priority)

| Keyword Cluster | Target Page | Notes |
|----------------|-------------|-------|
| "OpenLEG vs LEGHub" | /vergleich (new) | Only if strategically sound |
| "SDAT-CH Implementierung" | /api/v1/docs | Niche B2B, defer |
| "Smart Meter Kosten Schweiz" | /fuer-bewohner | Informational |
| "Netzbetreiber Transparenz" | /transparenz | Niche but authoritative |

---

## Implementation Phases

### Phase 1: Quick Wins (Week 1-2)

**Goal:** Fix technical SEO foundations. No new pages needed.

- [x] **SEO-1**: Add canonical tags to `gemeinde/profil.html` template ✅ 2026-03-05
- [x] **SEO-2**: Add LocalPlace JSON-LD schema to profil.html (name, description, geo coordinates, areaServed) ✅ 2026-03-05
- [x] **SEO-3**: Optimize profil.html H1: "Stromtarif in {{ name }}: {{ tariff }} Rp/kWh" ✅ 2026-03-05
- [x] **SEO-4**: Add meta tags to `gemeinde/verzeichnis.html` (title, description, canonical) ✅ 2026-03-05
- [x] **SEO-5**: Add CollectionPage schema to verzeichnis.html ✅ 2026-03-05
- [x] **SEO-6**: Add og:image fallback to all pages (use static og-image.png if no dynamic image) ✅ 2026-03-05
- [ ] **SEO-7**: Verify Google Search Console setup (submit sitemap)
- [x] **SEO-8**: Add BreadcrumbList schema to profil and verzeichnis pages ✅ 2026-03-05

### Phase 2: Formation Content (Week 3-4)

**Goal:** Capture formation-intent queries with a dedicated guide.

- [x] **SEO-9**: Create `/leg-gruenden` page: 5-step LEG formation guide ✅ 2026-03-05
- [x] **SEO-10**: Add HowTo schema to formation guide (schema.org/HowTo) ✅ 2026-03-05
- [ ] **SEO-11**: Add FAQ schema to formation guide (additional questions beyond fuer-bewohner)
- [ ] **SEO-12**: Internal linking: fuer-bewohner → leg-gruenden, fuer-gemeinden → leg-gruenden, profil → leg-gruenden
- [x] **SEO-13**: Create `/leg-kalkulator` page: interactive savings calculator ✅ 2026-03-05
- [x] **SEO-14b**: Create `/pilotgemeinde/baden` case study page with real BFS 4021 data (Article + Place schema) ✅ 2026-03-07

### Phase 3: Canton Expansion (Week 5-8)

**Goal:** Own "[Kanton] + LEG/Stromgemeinschaft" queries.

- [ ] **SEO-14**: Create `/leg/{kanton}` pages for top 10 cantons (ZH, BE, AG, LU, SG, BL, SO, TG, ZG, GR)
- [ ] **SEO-15**: Each canton page includes: canton-level tariff summary, municipality directory filtered by canton, LEG formation stats, link to cantonal energy office
- [ ] **SEO-16**: Add Kanton pages to sitemap
- [ ] **SEO-17**: Optimize profil pages with canton-specific internal links

### Phase 4: Authority Content (Week 8-12)

- [ ] **SEO-18**: Create `/developers` API landing page with schema.org/API markup
- [ ] **SEO-19**: Blog/Ratgeber section: "Was ist eine LEG?", "LEG vs ZEV: der Unterschied", "Mantelerlass 2026: was Gemeinden wissen müssen"
- [ ] **SEO-20**: Competitor comparison page (if strategically sound, respectful tone)

---

## Content Templates

### Municipality Profile Page (Phase 1)

```
H1: Stromtarif in {Gemeinde} 2026: {X} Rp/kWh | LEG-Ersparnis: CHF {Y}/Jahr
H2: Netztarif-Details
H2: Solarpotenzial in {Gemeinde}
H2: LEG-Potenzial: {N} mögliche Stromgemeinschaften
H2: So gründen Sie eine LEG in {Gemeinde}
CTA: Adresse prüfen → /fuer-bewohner
Schema: LocalPlace + BreadcrumbList
```

### Canton Landing Page (Phase 3)

```
H1: Lokale Stromgemeinschaften im Kanton {Kanton}
H2: Netztarife: Durchschnitt {X} Rp/kWh, Spanne {min}-{max}
H2: {N} Gemeinden mit LEG-Potenzial
H2: Solarpotenzial im Kanton {Kanton}
H2: LEG gründen im Kanton {Kanton}: Schritt für Schritt
Table: Top 10 Gemeinden nach LEG-Potenzial
CTA: Gemeinde-Verzeichnis → /gemeinde/verzeichnis?kanton={kanton}
Schema: CollectionPage + BreadcrumbList
```

### Formation Guide (Phase 2)

```
H1: LEG gründen: Anleitung in 8 Schritten
H2: 1. Nachbarn finden (DBSCAN-Matching)
H2: 2. Gemeinschaft bilden (min. 3 Teilnehmer)
H2: 3. Solarpotenzial prüfen (5% Mindestanteil)
H2: 4. Vereinbarung erstellen (Art. 17e StromVG)
H2: 5. Smart Meter beantragen (VNB installiert in 3 Monaten)
H2: 6. Beim Netzbetreiber anmelden
H2: 7. Abrechnung einrichten (15-Min-Intervalle)
H2: 8. LEG aktivieren
FAQ: 5-7 additional questions
Schema: HowTo + FAQPage
```

---

## Competitive SEO Position

| Factor | OpenLEG | LEGHub | smart-me | OWT |
|--------|---------|--------|----------|-----|
| Public pages | 2131+ | ~5 | ~20 | ~10 |
| Swiss tariff data | All 631 DSOs | None public | None | None |
| Schema markup | Partial (improving) | Unknown | Basic | Unknown |
| German content | Strong | Strong | Good | Weak |
| French content | None | None | None | Strong |
| Long-tail coverage | High potential | None | None | None |
| Developer content | API docs exist | None public | Some | None |

**OpenLEG's moat:** 2131 data-rich municipality pages that nobody else has. Competitors can't replicate without building the same data pipeline.

---

## Monitoring

- [ ] Set up Google Search Console
- [ ] Track: indexed pages, impressions, clicks, average position
- [ ] Weekly check: which municipality profiles are getting impressions
- [ ] Monthly: keyword ranking report for Tier 1 keywords
- [ ] Quarterly: content gap analysis refresh

---

## Budget

CHF 0. No paid ads. No paid tools. All organic.
Google Search Console: free. Schema validation: free. Content: written by AI + human review.
