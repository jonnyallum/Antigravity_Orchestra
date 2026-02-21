# Deadline Registration & Tracking Methodology

> **Goal**: Ensure every project milestone and dependency is tracked with deterministic alert thresholds.

---

## SOP-001: Deadline Registration

**Trigger:** New deadline identified in brief or project plan.

1. **Create Deadline Entry**: Document in `deadlines.json` or project board.
2. **Identify Dependencies**: List all tasks that must finish _before_ this deadline.
3. **Set Alert Thresholds**:
   - 🟠 **Warning**: 48 hours before.
   - 🔴 **Critical**: 12 hours before.
4. **Assign Owner**: Post a NEXT_HOP to the specialist responsible.
5. **Add to Shared Brain**: Sync the deadline status via `jonnyai-mcp`.

## SOP-002: Approaching Deadline Protocol

**Trigger:** Deadline enters the "Warning" (48h) window.

1. **Notify Owner**: Post a status ping in `chatroom.md`.
2. **Check Task Status**: Verify if PAYLOAD_PATH exists and is current.
3. **Identify Blockers**: If not IN_PROGRESS, ask for the blocker reason.
4. **Escalate**: If status is BLOCKED, assign NEXT_HOP to @Marcus for resource reallocation.

## SOP-003: Missed Deadline Protocol

**Trigger:** Deadline passed without GATE_CLEARED.

1. **Immediately Notify @Marcus**: Post an emergency state packet.
2. **Document Reason**: First responder captures the "why" in incident log.
3. **Set Recovery Date**: Propose a new deterministic deadline.
4. **Stakeholder Update**: Notify affected agents via NEXT_HOP.

---

_Jai.OS 4.0 | Method Library | Registered_
