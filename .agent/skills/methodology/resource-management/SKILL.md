# Agency Resource & Workload Management

> **Goal**: Optimize agent distribution across projects to prevent bottlenecks and ensure mission-critical lanes are always staffed.

---

## SOP-001: Weekly Resource Review

**Trigger:** Every Monday (Session Start).

1. **Review Project Health**: Scan all active projects in Supabase.
2. **Check Agent Workload**: Query `task-history.json` for task density per handle.
3. **Identify Bottlenecks**: Flag agents with >3 active P0 NEXT_HOP assignments.
4. **Propose Reallocation**: Recommend shifting specialists (e.g., @Sebastian from Project A to B).
5. **Update Capacity Forecast**: Post summary to `chatroom.md`.

## SOP-002: New Project Intake

**Trigger:** Approved project brief from @Jonny.

1. **Requirement Estimate**: List required skills (e.g., UI, DB, SEO).
2. **Availability Check**: Verify which specialists have open capacity.
3. **Draft Team**: Propose a "Strike Team" for the project.
4. **Flag Risks**: Mention if critical agents (e.g., @Adrian) are over-leveraged.

## SOP-003: Resource Conflict Resolution

**Trigger:** Two projects require the same specialist simultaneously.

1. **Assess Priority**: Compare project impact and @Jonny's current focus.
2. **Evaluate Impact**: What is the delay if one project waits?
3. **Strategy Recommendation**: Propose a split (50/50) or a "Forced March" (100% on priority).
4. **@Marcus Sign-off**: Escalation to Command Tier for deterministic decision.

---

_Jai.OS 4.0 | Method Library | Resource Management_
