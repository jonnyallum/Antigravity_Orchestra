---
description: The master collaboration and delegation enforcement directive. Ensures every agent action produces a closed feedback loop and every task is routed to the right specialist.
enforced_by: "@Marcus (Conductor), @Vigil (The Eye)"
version: "2.0"
created: 2026-02-07
updated: 2026-02-09
changelog: "v2.0 — Added delegation protocol, routing matrix, handover templates, context-loading mandate, memory integration"
---

# 🔗 Collaboration & Delegation Enforcement Directive

> **The Rule:** Every action must close a loop. Every task must be routed to the right specialist. No orphaned work. No silent completions. No unacknowledged handovers.

## The Problem This Solves

The Jai.OS 4.0 ecosystem has 44 agents across multiple AI environments (Claude, Gemini, Cline). Without enforced collaboration loops AND smart delegation, work gets:
- **Duplicated** — two agents solve the same problem independently
- **Dropped** — handover messages are sent but never read
- **Unlearned** — incidents are fixed but the fix is never captured
- **Invisible** — major work happens with no chatroom trace
- **Misrouted** — generalists attempt specialist work, producing mediocre output
- **Context-starved** — agents start tasks without reading what came before

---

## Part 1: The Delegation Protocol (NEW in v2.0)

### The Routing Decision Tree

Before starting ANY task, the executing AI must answer:

```
1. What TYPE of task is this? (design, backend, deploy, security, data, copy, etc.)
2. Which SPECIALIST owns this domain? (Check routing matrix below)
3. Do I have the CONTEXT? (Check memory banks, task history, chatroom)
4. Is the specialist AVAILABLE? (Check agent-health.json status)
5. Am I the RIGHT agent for this? (If not, ROUTE — don't attempt)
```

### The Routing Matrix

| Task Type | Primary Agent | Backup Agent | Never Assign To |
|:----------|:-------------|:-------------|:----------------|
| **Architecture / Backend** | @Sebastian | @Cline | @Priya, @Elena |
| **UI/UX Design** | @Priya | @Vivienne | @Sebastian, @Sam |
| **Database / Schema** | @Diana | @Steve | @Owen, @Elena |
| **Deployment** | @Owen | @Derek | @Priya, @Felix |
| **Security Audit** | @Sam | @Vigil | @Felix, @Elena |
| **SEO / Meta** | @Grace | @Elena | @Sam, @Diana |
| **Copywriting / Tone** | @Elena | @Rowan | @Sebastian, @Diana |
| **Truth Verification** | @Rowan | @Vigil | @Felix, @Owen |
| **Monetization** | @Felix | @Jasper | @Sam, @Owen |
| **CI/CD / Automation** | @Alex | @Derek | @Priya, @Elena |
| **Research / Intel** | @Sophie | @Rowan | @Owen, @Derek |
| **Parallel Learning** | @Coordinator-L | @Marcus | Any non-PLR agent |
| **Branding / Identity** | @Vivienne | @Blaise | @Sam, @Diana |
| **Mobile Optimization** | @Milo | @Priya | @Diana, @Derek |
| **Supabase Specialist** | @Steve | @Diana | @Owen, @Elena |
| **Quality Monitoring** | @Vigil | @Sam | @Felix, @Elena |
| **Orchestration** | @Marcus | N/A | Everyone else |

### Delegation Rules

1. **Route, Don't Attempt** — If a task falls outside your domain, route it to the specialist. Don't produce a "good enough" version.

2. **Context Handover Required** — When routing, include:
   - What needs to be done (1-2 sentences)
   - Why it needs to be done (business context)
   - What's already been done (link to files/commits)
   - What the success criteria are
   - Any constraints or deadlines

3. **Acknowledge Within 1 Turn** — When receiving a routed task, acknowledge with:
   - "ACCEPTED: [brief plan]" or
   - "DECLINED: [reason + suggested alternative]"

4. **No Chain Delegation** — If Agent A routes to Agent B, Agent B cannot re-route to Agent C without Agent A's knowledge. Escalate to @Marcus instead.

5. **Specialist Override** — A specialist can override a generalist's work in their domain without asking. But they must document what they changed and why.

### The Handover Template

When routing work between agents, use this format in chatroom or message files:

```markdown
## 🔄 HANDOVER: [Task Name]
**From:** @[Sender] → **To:** @[Receiver]
**Priority:** P0/P1/P2/P3
**Context:** [1-2 sentences on what and why]
**Files:** [List of relevant files]
**Done So Far:** [What's already been completed]
**Needs:** [What the receiver needs to do]
**Success Criteria:** [How we know it's done]
**Deadline:** [If applicable]
```

---

## Part 2: The Context-Loading Mandate (NEW in v2.0)

### Before ANY Work Begins

Every AI session must execute the Session Start Checklist (`directives/session_start_checklist.md`):

1. Check `.tmp/message4[ai].md` for pending messages
2. Check `.agent/boardroom/chatroom.md` for recent activity
3. Read `CLINE_SYNC.md` and `.tmp/memory_banks/active_context.md`
4. Scan `.agent/memory/agent-health.json` for critical gaps
5. Read last 5 tasks from `.agent/memory/task-history.json`

**Violation:** Starting work without context-loading = working blind. The output will be rejected.

### Before ANY Specialist Work

When entering a specialist's domain, additionally:

1. Read the specialist's `SKILL.md` (capabilities, restrictions, SOPs)
2. Check if they have pending work in the same area
3. Check `.agent/memory/learning-runs.json` for relevant PLR insights

---

## Part 3: The 5 Mandatory Loops (Updated)

### Loop 1: Message → Acknowledge → Complete
**Directive:** `directives/inter_ai_communication.md`

Every `.tmp/message4[agent].md` must progress through:
```
AWAITING_ACK → ACKNOWLEDGED → COMPLETED
```
**Violation:** A message stuck at `AWAITING_ACK` for >2 hours triggers @Marcus escalation.

### Loop 2: Task → Log → Learn
**Tool:** `execution/feedback_engine.py` + `execution/memory_quality_gate.py`

Every significant task must be logged:
```bash
# Log the task
python execution/feedback_engine.py log [agent] [type] [success] --learning="[insight]"

# If a learning was discovered, validate it before storing
python execution/memory_quality_gate.py validate --learning "[insight]" --source "T0XX" --confidence 0.9
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

### Loop 6: Delegate → Acknowledge → Deliver → Close (NEW)

Every delegation must complete the full cycle:
```
ROUTED → ACKNOWLEDGED → IN_PROGRESS → DELIVERED → VERIFIED → CLOSED
```

**Violation:** A delegation stuck at ROUTED for >1 turn = @Marcus escalation. A delivery without verification = not done.

---

## Part 4: Enforcement Mechanism

### Automated Checks
- `execution/feedback_engine.py gaps` — detects agents with low logging rates
- `execution/validate_agents.py` — checks SKILL.md compliance
- `execution/orchestra_heartbeat.py` — detects idle/ghosted agents
- `execution/memory_quality_gate.py report` — memory health dashboard

### Manual Checks (Weekly Sprint Review)
@Marcus reviews during Sprint Review:
1. Are all `.tmp/message4*.md` files at `COMPLETED` status?
2. Does the feedback engine show logging activity for all active agents?
3. Are there any incidents without corresponding SKILL.md updates?
4. Are there Team Talks without meeting minutes?
5. **NEW:** Were any tasks misrouted? (generalist doing specialist work)
6. **NEW:** Are there delegation chains longer than 2 hops?
7. **NEW:** Did all sessions start with context-loading?

### Escalation
| Violation Count | Action |
|:----------------|:-------|
| 1st | @Marcus flags in chatroom |
| 2nd | @Vigil adds to quality scan watchlist |
| 3rd | @Marcus escalates to Jonny (The Boss) |

---

## Quick Reference: "Did I Close the Loop?"

Before ending your turn, every agent should verify:

- [ ] **Routed correctly** — Did I check the routing matrix before starting?
- [ ] **Context loaded** — Did I read memory banks and task history?
- [ ] **Chatroom updated** — Did I post what I did?
- [ ] **Feedback logged** — Did I run `feedback_engine.py log`?
- [ ] **Learning captured** — Did I run `memory_quality_gate.py validate` if I learned something?
- [ ] **Messages acknowledged** — Did I ACK any pending messages?
- [ ] **SKILL.md updated** — Did I learn something worth capturing?
- [ ] **Handover written** — If another agent needs to continue, did I write the handover?
- [ ] **Memory banks updated** — Did I update active_context.md if priorities changed?

**If any box is unchecked, you're not done.**

---
*Enforced by @Marcus and @Vigil | v2.0 Updated: 2026-02-09 | Jai.OS 4.0*
