---
description: When and how to trigger a Team Talk swarm to unblock work or solve complex problems.
updated: 2026-02-07
version: "2.0 (Jai.OS 4.0 Aligned)"
---

# Team Talk (Swarm) Trigger Protocol

A **Team Talk** is a synchronous multi-agent swarm. We trigger it when single-agent execution risks failure, hallucination, or low quality.

## When to Call a Team Talk

1. **Cross-Domain Blockers**: e.g., "The mobile build failed (@Milo) because the API schema changed (@Steve)."
2. **Architecture Decisions**: e.g., "Designing a new monetization funnel (@Felix + @Sebastian + @Diana)."
3. **Quality Crisis**: e.g., "@Vigil says the app feels 'cheap' → Call @Priya (Design) + @Elena (Copy) + @Milo (Mobile)."
4. **Unknown Unknowns**: e.g., "We need to cut costs but don't know how → Call @Felix (Monetization) + @Sophie (Research)."
5. **Production Incident**: e.g., "Live site is down → Call @Owen (Deploy) + @Sam (Security) + @Derek (Infra)."
6. **Truth-Lock Violation**: e.g., "Placeholder content shipped → Call @Rowan (Truth) + @Vigil (Verification) + @Priya (Design)."

## The Swarm Ritual

### 1. The Signal
@Marcus asserts: **"TRIGGERING TEAM TALK: [Problem Statement]."**

### 2. The Roll Call
@Marcus names the attendees using their **human handles** (Jai.OS 4.0 standard).

*Example*: "Attendance: @Sebastian (Architecture), @Steve (Backend), @Milo (Mobile)."

### 3. The Synthesis
Each agent provides a **<100 word update** from their persona's perspective. Must include:
- Current state of their domain relative to the problem
- One concrete recommendation
- Any blockers they need resolved

### 4. The Resolution
The swarm agrees on a unified plan. @Marcus documents:
- **Decision**: What was decided
- **Action Items**: Who does what by when
- **Learning**: What gets captured in SKILL.md

### 5. The Close-Out
@Marcus posts the resolution to:
- `.agent/boardroom/chatroom.md` (summary)
- `.agent/boardroom/meetings/YYYY-MM-DD-team-talk-[topic].md` (full minutes)
- Relevant agent SKILL.md files (learnings)

## Summoning Matrix (Jai.OS 4.0)

| Problem Domain | Required Agents | Optional |
|:---------------|:----------------|:---------|
| Frontend Blocker | @Marcus, @Sebastian, @Priya | @Milo, @Blaise |
| Backend/API Issue | @Marcus, @Sebastian, @Diana | @Steve, @Sam |
| Deployment Failure | @Marcus, @Owen, @Derek | @Sam, @Alex |
| Security Incident | @Marcus, @Sam, @Victor | @Diana, @Owen |
| Content Quality | @Marcus, @Rowan, @Elena | @Vigil, @Priya |
| SEO/Visibility | @Marcus, @Grace, @Elena | @Sophie, @Rowan |
| Monetization | @Marcus, @Felix, @Sebastian | @Diana, @Elena |
| Mobile Issue | @Marcus, @Milo, @Priya | @Sebastian, @Blaise |
| Betting Algorithm | @Marcus, @Cline, @Bookie | @Gaffer, @Handicapper |
| Trading System | @Marcus, @Delboy, @Sebastian | @Sam, @Victor |

## Self-Annealing (Post-Resolution)

After every Team Talk that solves a novel problem:

1. **Extract the solution pattern** — what was the root cause and fix?
2. **Update the relevant Agent's `SKILL.md`** with a new learning entry
3. **Log to feedback engine**: `python execution/feedback_engine.py log [agent] team-talk true --learning="[pattern]"`
4. **Update methodology** if the pattern applies broadly (`.agent/skills/methodology/`)
5. **Create runbook** if the issue could recur (`docs/runbooks/[topic].md`)

## Feedback Loop Integration

Every Team Talk MUST produce:
- [ ] Meeting minutes in `.agent/boardroom/meetings/`
- [ ] At least one SKILL.md update
- [ ] A feedback engine log entry
- [ ] A chatroom summary post

**Failure to close the loop = the Team Talk didn't happen.**

---
*Enforced by @Marcus (Conductor) | Updated: 2026-02-07 | Jai.OS 4.0*
