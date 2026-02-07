---
description: The Truth-Lock Protocol — mandatory verification gate for all production output.
enforced_by: "@Vigil (The Eye), @Rowan (The Beast)"
---

# 🔒 Truth-Lock Protocol

> No production claim, design, or data output is final until verified.

## Purpose

Truth-Lock prevents "Probabilistic Drift" — the tendency for AI agents to generate plausible-sounding but unverified content, placeholder data, or fabricated statistics. Every deliverable that touches production must pass through a verification gate.

## Scope

This protocol applies to:
- **Content**: Any text, copy, or claims published on client websites
- **Data**: Any records written to Supabase (predictions, leads, analytics)
- **Code**: Any deployment to production hosting (Vercel, Hostinger)
- **Design**: Any UI component marked as "final" or "shipped"

## Verification Gates

### Gate 1: Source Verification (@Vigil)
- Every factual claim must have a traceable source
- Statistics must reference the dataset, date range, and methodology
- "Conviction scores" in betting must be calculated, never randomized
- **Fail condition**: Any use of `random.*` in production prediction generators

### Gate 2: Content Integrity (@Rowan)
- No placeholder text (Lorem ipsum, "Coming soon", generic descriptions)
- No fabricated testimonials or case studies
- Brand voice must match the client's tone guide
- **Fail condition**: Latin text or generic stock copy in any shipped component

### Gate 3: Technical Verification (@Sam / @Sentinel)
- Code compiles and passes lint
- No exposed API keys, secrets, or credentials in committed code
- RLS policies enabled on all Supabase tables with user data
- **Fail condition**: Any `.env` values committed to git

## Enforcement

| Violation | Severity | Action |
|:----------|:---------|:-------|
| Placeholder text in production | P0 | Immediate rollback, incident report |
| Randomized data tagged as "prediction" | P0 | Script quarantine, DB cleanup |
| Missing source on factual claim | P1 | Content held until source provided |
| Generic UI (no brand customization) | P2 | Flagged for @Priya review |

## Incident Response

When a Truth-Lock violation is detected:
1. **Log** the incident in `.agent/memory/incidents/`
2. **Quarantine** the offending script or content
3. **Fix** the root cause (not just the symptom)
4. **Update** the relevant `SKILL.md` with the learning
5. **Verify** the fix passes all three gates

## Historical Incidents

| Date | Incident | Resolution |
|:-----|:---------|:-----------|
| 2026-02-05 | Placeholder text shipped to DJ Waste production | Content-Preservation Protocol created |
| 2026-02-06 | Gaffer_v3.0 used random.sample() for betting predictions | Opus Standard established, script quarantined |

---
*Enforced by @Vigil and @Rowan | Standardized: 2026-02-07 | AgOS 3.0*
