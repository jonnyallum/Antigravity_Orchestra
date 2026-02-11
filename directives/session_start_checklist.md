# Session Start Checklist — Mandatory Protocol
> Jai.OS 4.0 | Effective: 2026-02-09

## Purpose
Every AI session (Cline, Claude, Gemini) MUST execute this checklist before doing any work. This prevents context loss, stale decisions, and memory amnesia.

---

## The Checklist (Execute in Order)

### 1. 📬 Check Messages
- Read `.tmp/message4[your-ai].md`
- If status is not CLEAR, handle the pending message first
- Mark as CLEAR when done

### 2. 💬 Check Chatroom
- Read `.agent/boardroom/chatroom.md` (last 20 lines)
- Note any unresolved threads or @mentions

### 3. 🧠 Load Context
- Read `CLINE_SYNC.md` (or equivalent for your platform)
- Read `.tmp/memory_banks/active_context.md`
- Note current focus, blockers, and priorities

### 4. 📊 Check Health
- Scan `.agent/memory/agent-health.json` summary section
- Note any gaps_detected with severity "critical"

### 5. 📋 Check Task History
- Read `.agent/memory/task-history.json` last 5 tasks
- Understand what was done recently and what failed

### 6. 🎯 Confirm Mission
- Ask user for today's objective (or check pending tasks)
- Route to correct agent persona per AGENTS.md

---

## After Every Task

### 7. 📝 Log the Outcome
- Add task to `.agent/memory/task-history.json`
- Update `.agent/memory/agent-health.json` for the assigned agent
- If learning discovered: run `python execution/memory_quality_gate.py validate`

### 8. 🔄 Update Context
- Update `.tmp/memory_banks/active_context.md` if priorities changed
- Update `CLINE_SYNC.md` with session summary
- Clear or update `.tmp/message4[ai].md`

---

## Why This Matters

Without this checklist, every session starts from scratch. The system has 43 agents, 9 clients, 4 ecosystems, and 100+ execution scripts. Context loss = wasted time, repeated mistakes, and degraded quality.

**The memory layer only works if we actively read from it AND write to it.**

---

*Directive created: 2026-02-09 | Source: Full System Audit (AUDIT-001)*
