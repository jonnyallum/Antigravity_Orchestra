
# 🤖 Project Task for @Cline
> **Objective:** Sync @Cline with the Kwizz.co.uk AgOS 3.0 workspace for collaborative development.
> **Last Synced:** 2026-02-06T19:28:00Z | **Status:** ✅ SYNCED & OPERATIONAL

## 1. Setup Phase
- [x] **Read Memory:** Reviewed `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` — 4-layer Hive Mind Architecture absorbed.
- [x] **Activate Tools:** MCP server verified. `fastmcp 2.14.4`, `mcp 1.26.0`, `supabase 2.15.1` all installed.
  - `.mcp.json` configured with Supabase HTTP MCP endpoint.
  - `execution/mcp_supabase_kwizz.py` ready (FastMCP server with 4 tools: `list_quizzes`, `get_quiz_details`, `create_quiz_pack`, `get_active_games`).
- [x] **Supabase Connectivity:** REST API confirmed live — returning quiz data (5+ packs verified).
  - ⚠️ **Note:** Direct PostgreSQL connection (`db.japkqygktnubcrmlttqt.supabase.co`) DNS fails (free-tier paused). REST API works fine.
  - Self-annealed `check_kwizz_supabase.py` to use REST API instead.

## 2. Collaborative Objectives
- [ ] **UI Polish:** Assist @Pixel in upgrading `host/page.tsx` and `play/page.tsx` with high-velocity Framer Motion animations.
- [ ] **Content Engine:** Help @Conductor monitor the `bulk_import_trivia.py` runs and verify data integrity via MCP.
- [ ] **Security:** Support @Sam in implementing Google Auth logic in the frontend.

## 3. The Rules of Engagement
1. **Sync Before Strike:** Always read `.agent/skills/` before working in a specific agent's domain.
2. **Deterministic-First:** If a task can be a Python script in `execution/`, build it there instead of doing manual code edits.
3. **No Placeholders:** If you need content, use the MCP to fetch real data from Supabase.

## 4. How to Sync
1. ~~Run `python execution/validate_agents.py` to verify your environment.~~ ✅ Ran — 41 agents found (14 valid AgOS 2.0 format, 27 in AgOS 3.0 format — validator needs upgrade).
2. ~~Run `python execution/check_kwizz_supabase.py` to confirm DB connection.~~ ✅ REST API confirmed live. Script self-annealed.
3. Access tools via the configured MCP server.

## 5. @Cline Context Map (What I Know)

### Architecture
- **AgOS 3.0 Hive Mind:** 4 layers — Talent → Boardroom → Engine → Memory
- **39-Agent Orchestra** with key handles: @Marcus (Conductor), @Sebastian (Architect), @Priya (Designer), @Sam (Security), @Diana (Database), @Steve (Supabase), @Vigil (Verification), @Owen (Deployment)

### Kwizz Project State
- **Phase 1-3:** ✅ Complete (Foundation, Quiz Engine, Real-Time Host/Player)
- **Phase 4:** 🔄 In Progress (God-Tier Polish)
  - Task 4.1: Public Deployment — Pending
  - Task 4.2: Audio Experience (SFX) — Pending
  - Task 4.3: PWA Transformation — Pending
  - Task 4.4: Advanced Host Features — Pending
  - Task 4.5: QR Fix — ✅ Done
- **Phase 5: Monetization** ✅ Strategy & Schema Complete
  - Task 5.1: MONETIZATION_STRATEGY.md v2.0 — ✅ "3 Doors" model (Free/Credits/Unlimited)
  - Task 5.2: Supabase monetization schema — ✅ 7 tables, RLS, helper functions
  - Task 5.3: Pricing page UI — ✅ `/pricing` route with animated 3-card layout
  - Task 5.4: Apply schema to Supabase — Pending (@Diana/@Steve)
  - Task 5.5: Stripe integration — Pending (@Sebastian)
  - Task 5.6: Credit deduction gate — Pending (@Sebastian)
  - Task 5.7: Player Prime cosmetics UI — Pending (@Priya)

### Codebase Familiarity
| File | Status | Notes |
|:-----|:-------|:------|
| `app/page.tsx` | ✅ Read & Updated | Home page — Added "Pricing" link with CreditCard icon |
| `app/pricing/page.tsx` | ✅ Created | "3 Doors" pricing page — Free Trial, Pay As You Go, Unlimited + Corporate CTA |
| `supabase_monetization_schema.sql` | ✅ Created | 7 tables, RLS policies, `check_host_access()` + `deduct_credit()` functions |
| `MONETIZATION_STRATEGY.md` | ✅ Rewritten | v2.0 — "3 Doors" pricing, revenue projections, 90-day launch plan |
| `app/host/page.tsx` | ✅ Read | Host dashboard — Lobby (QR+PIN), Active Game (questions/responses), Finished (leaderboard) |
| `app/play/page.tsx` | ✅ Read | Player interface — Join form, Lobby wait, Buzzer, Finished rank |
| `app/select/page.tsx` | ✅ Read | Quiz selector — Category filter, quiz grid, "Sync & Launch" |
| `app/globals.css` | ✅ Read | Tailwind v4 theme — Obsidian, Electric Purple, Neon Cyan, glassmorphism utilities |
| `lib/useGameSync.ts` | ✅ Read | Supabase Realtime hook — game/player/response sync, CRUD functions |
| `lib/supabase.ts` | ✅ Located | Supabase client init |
| `execution/mcp_supabase_kwizz.py` | ✅ Read | FastMCP server with 4 tools |
| `execution/check_kwizz_supabase.py` | ✅ Read & Fixed | Self-annealed to use REST API |

### Known Issues
1. **Buzzer timing is placeholder:** `play/page.tsx` line ~55 uses `Math.random() * 3000` instead of actual timing — needs real implementation.
2. **Direct DB connection fails:** Free-tier Supabase pauses direct PostgreSQL. All scripts should use REST API.
3. **Agent validator expects AgOS 2.0 format:** `validate_agents.py` needs updating for AgOS 3.0 SKILL.md structure.

---
*Generated by @Conductor for @Cline | Updated by @Cline on sync*
