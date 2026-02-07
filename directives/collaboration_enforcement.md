---
description: The master collaboration enforcement directive. Ensures every agent action produces a closed feedback loop.
enforced_by: "@Marcus (Conductor), @Vigil (The Eye)"
version: "1.0"
created: 2026-02-07
---

# 🔗 Collaboration Enforcement Directive

> **The Rule:** Every action must close a loop. No orphaned work. No silent completions. No unacknowledged handovers.

## The Problem This Solves

The Jai.OS 4.0 ecosystem has 40 agents across multiple AI environments (Claude, Gemini, Cline, ChatGPT). Without enforced collaboration loops, work gets:
- **Duplicated** — two agents solve the same problem independently
- **Dropped** — handover messages are sent but never read
- **Unlearned** — incidents are fixed but the fix is never captured
- **Invisible** — major work happens with no chatroom trace

## The 5 Mandatory Loops

### Loop 1: Message → Acknowledge → Complete
**Directive:** `directives/inter_ai_communication.md`

Every `.tmp/message4[agent].md` must progress through:
```
AWAITING_ACK → ACKNOWLEDGED → COMPLETED
```
**Violation:** A message stuck at `AWAITING_ACK` for >2 hours triggers @Marcus escalation.

### Loop 2: Task → Log → Learn
**Tool:** `execution/feedback_engine.py`

Every significant task must be logged:
```bash
python execution/feedback_engine.py log [agent] [type] [success] --learning="[insight]"
```
**Violation:** A deployment, incident, or Team Talk without a feedback log entry = the work didn't happen.

### Loop 3: Incident → Fix → Update SKILL.md
**Directive:** `directives/truth_lock_protocol.md`

Every incident must produce:
1. An incident file in `.agent/memory/incidents/`
2. A root cause fix (not just a symptom patch)
3. A SKILL.md update for the responsible agent
4. A methodology update if broadly applicable

**Violation:** An incident without a SKILL.md update = the system didn't learn.

### Loop 4: Team Talk → Minutes → Action Items
**Directive:** `directives/team_talk_triggers.md`

Every Team Talk must produce:
1. Meeting minutes in `.agent/boardroom/meetings/`
2. Action items with owners and deadlines
3. At least one SKILL.md learning entry
4. A chatroom summary post

**Violation:** A Team Talk without minutes = the meeting didn't happen.

### Loop 5: Deploy → Sign-Off → Verify
**Protocol:** `.agent/boardroom/templates/sign-off.md`

Every deployment must have:
1. All 8 quality gates passed (Design, Mobile, Truth, Content, SEO, Security, Data, Deploy)
2. A `SIGN_OFF.md` in the project directory
3. Post-deploy verification (live site check)

**Violation:** A deployment without sign-off = unauthorized release.

## Enforcement Mechanism

### Automated Checks
- `execution/feedback_engine.py gaps` — detects agents with low logging rates
- `execution/validate_agents.py` — checks SKILL.md compliance
- `execution/orchestra_heartbeat.py` — detects idle/ghosted agents

### Manual Checks (Weekly Sprint Review)
@Marcus reviews during Sprint Review:
1. Are all `.tmp/message4*.md` files at `COMPLETED` status?
2. Does the feedback engine show logging activity for all active agents?
3. Are there any incidents without corresponding SKILL.md updates?
4. Are there Team Talks without meeting minutes?

### Escalation
| Violation Count | Action |
|:----------------|:-------|
| 1st | @Marcus flags in chatroom |
| 2nd | @Vigil adds to quality scan watchlist |
| 3rd | @Marcus escalates to Jonny (The Boss) |

## Quick Reference: "Did I Close the Loop?"

Before ending your turn, every agent should verify:

- [ ] **Chatroom updated** — Did I post what I did?
- [ ] **Feedback logged** — Did I run `feedback_engine.py log`?
- [ ] **Messages acknowledged** — Did I ACK any pending messages?
- [ ] **SKILL.md updated** — Did I learn something worth capturing?
- [ ] **Handover written** — If another agent needs to continue, did I write the message?

**If any box is unchecked, you're not done.**

---
*Enforced by @Marcus and @Vigil | Created: 2026-02-07 | Jai.OS 4.0*
