# PRD: DeerFlow Pattern Extraction

**Status:** Active
**Priority:** P2
**Date:** 2026-03-07
**Source:** ByteDance DeerFlow v2 (github.com/bytedance/deer-flow)

## Decision

After deep truth analysis with 4 independent evaluation tracks (structural, fit, strategic, forensic), all converged: do NOT adopt DeerFlow as a framework. Extract 3 specific patterns at low cost.

Decision filter applied: "Does this help a citizen discover or form a LEG?"
- Research cron: yes (indirectly, via BFE grants and regulatory awareness)
- Prompt patterns: yes (better municipality analysis quality)
- Full DeerFlow sidecar: no (tech for tech's sake at zero users)

## Extracted Patterns (Implemented)

### 1. Plan-Research-Synthesize Decomposition
- **Applied to:** `openclaw/workspace/SOUL.md` analysis protocol
- **DeerFlow source:** Planner, Researcher, Reporter agent pipeline
- **Our adaptation:** prompt-level 3-step protocol in workspace instructions. No StateGraph, no agent handoff. LEA follows structured reasoning via SOUL.md.
- **Effort:** 30 min

### 2. Automated Research Pipeline
- **Applied to:** `scripts/research_cron.py`, OpenClaw `weekly-research-scan` cron
- **DeerFlow source:** Researcher agent + web search tools + report synthesis
- **Our adaptation:** Brave Search API + Groq LLM (both already available). No langchain, no new deps. Uses `requests` only.
- **Effort:** 3h
- **Cost:** ~$0/week (Groq free tier + Brave free tier)

### 3. Structured Analysis Output
- **Applied to:** `openclaw/workspace/TOOLS.md` JSON schema
- **DeerFlow source:** Reporter agent structured output (Pydantic models)
- **Our adaptation:** JSON schema in workspace docs. Not code-enforced. LEA follows via prompt.
- **Effort:** 15 min

## Deferred Patterns

| Pattern | DeerFlow Component | Effort | Precondition |
|---------|-------------------|--------|-------------|
| StateGraph orchestration | LangGraph state machine, 11-stage middleware | 2-3 weeks | 3+ active municipalities needing multi-step automated workflows |
| Sandboxed code execution | Docker sandbox provider, path translation layer | 1 week | Academic users needing ad-hoc data analysis |
| Human-in-the-loop checkpoints | ClarificationMiddleware, SubagentLimitMiddleware | 3 days | Already partially covered by RED tier Telegram approvals |
| Report generation (PDF/MD) | Reporter agent, artifact system | 1 week | First real LEG formation requesting feasibility reports |
| Full multi-agent sidecar | 4-service architecture (Nginx, Frontend, Gateway, LangGraph) | 4-6 weeks | Post-funding, multiple concurrent research streams |
| Long-term memory system | MemoryMiddleware, .deer-flow/memory.json | 3 days | LEA quality issues from lack of cross-session context |
| Progressive skill loading | Skills system with frontmatter SKILL.md files | 2 days | Context window pressure from too many tools |
| Reflection/self-critique | Reflection loop in agent graph | 3 days | Measurable quality issues with current outputs |

## Why NOT Full DeerFlow

1. **Zero users.** Multi-agent complexity serves no one.
2. **Solo developer.** Maintenance burden of LangGraph + 4 new services.
3. **Budget.** DeerFlow assumes GPT-4+ pricing. OpenLEG uses Groq free tier.
4. **Feature freeze.** Cannot ship new product features until 3 municipalities active.
5. **Infrastructure overlap.** OpenClaw already provides LLM, search, cron, Telegram. DeerFlow duplicates 80%.
6. **Production failure rates.** 41-86.7% failure rate in multi-agent production systems (arXiv:2503.13657).
7. **ByteDance provenance.** Minor concern for Swiss civic infrastructure grant applications.

## Key Numbers from Analysis

- DeerFlow requires 4 services (Nginx:2026, Frontend:3000, Gateway:8001, LangGraph:2024)
- OpenLEG already runs 4 services (Flask, Postgres, OpenClaw, Caddy)
- Pattern extraction: ~6h total vs ~40-80h full integration
- 78% confidence: extract patterns, do not adopt framework
- Break-even on full integration: years (if ever)

## Revisit Criteria

Revisit this document when ANY of:
- 3+ municipalities have active registrations (feature freeze lifts)
- LEA research quality demonstrably insufficient (reflection pattern)
- Multiple concurrent research streams needed (StateGraph)
- BFE grant approved with engineering budget (full sidecar)
- Academic partnership requires sandboxed data analysis

## References

- DeerFlow GitHub: github.com/bytedance/deer-flow
- DeepWiki architecture: deepwiki.com/bytedance/deer-flow
- Multi-agent failure study: arxiv.org/pdf/2503.13657
- GitHub Blog on failures: github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail
