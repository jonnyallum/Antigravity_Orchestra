---
description: Emergency escalation protocols for critical failures. Defines halt conditions, rollback procedures, and incident response.
---

# Emergency Protocols (Jai.OS 4.0)

When things break at scale, the Orchestra needs a fire drill — not panic.

---

## 🚨 Severity Levels

| Level     | Name        | Definition                                           | Response Time              |
| :-------- | :---------- | :--------------------------------------------------- | :------------------------- |
| **SEV-1** | 🔴 Critical | Production site down, data loss, security breach     | Immediate — all work stops |
| **SEV-2** | 🟠 Major    | Broken deployment, API failures, client-facing bugs  | <30 minutes                |
| **SEV-3** | 🟡 Moderate | Non-blocking bugs, visual regressions, failing tests | <2 hours                   |
| **SEV-4** | 🔵 Minor    | Typos, minor styling issues, documentation gaps      | Next sprint                |

---

## 🛑 Automatic Halt Conditions

The following trigger an **immediate halt** — all agents pause current work:

1. **Production Site Down**: Any deployed client site returning 5xx errors.
   - **First Responder**: @Owen (The Hornet) + @Derek (The Engine)
   - **Escalation**: @Marcus → @Jonny

2. **Security Breach**: Exposed credentials, unauthorized access, or RLS bypass.
   - **First Responder**: @Victor (The Locksmith) + @Sam (The Gatekeeper)
   - **Escalation**: @Marcus → @Jonny → @Luna (Legal)

3. **Data Loss**: Supabase table corruption, accidental deletion, or migration failure.
   - **First Responder**: @Diana (The Vault) + @Steve (The Schema Whisperer)
   - **Escalation**: @Marcus → @Jonny

4. **Financial Error**: Incorrect Stripe charges, betting system malfunction, or fund misallocation.
   - **First Responder**: @Felix (The Alchemist) + @Sterling (The Bookie)
   - **Escalation**: @Marcus → @Jonny (IMMEDIATE)

---

## 🔄 Rollback Procedures

### Code Rollback

```bash
# Revert to last known good commit
git log --oneline -5              # Identify the target
git revert HEAD --no-commit       # Stage the revert
git commit -m "[ROLLBACK] SEV-X: [description]"
git push origin main
```

### Deployment Rollback

```bash
# Use the deploy workflow with rollback flag
# @Owen executes via /deploy [client] --rollback
```

### Database Rollback

- @Diana maintains point-in-time Supabase backups.
- Restore via Supabase Dashboard → Database → Backups.
- **Never** run destructive SQL without a backup confirmation.

---

## 📋 Incident Response Template

When an emergency occurs, the first responder posts this to `chatroom.md`:

```markdown
[TASK_ID]: INCIDENT-[DATE]-[SEV]
[CURRENT_STATE]: BLOCKED
[PAYLOAD_PATH]: .tmp/incidents/[incident-id].md
[NEXT_HOP]: @[first-responder]

**INCIDENT REPORT**

- **Severity**: SEV-[1/2/3/4]
- **Description**: [What happened]
- **Impact**: [What is affected]
- **First Responder**: @[handle]
- **Status**: [INVESTIGATING | MITIGATING | RESOLVED]
```

---

## 🔒 Post-Incident Protocol

After resolution:

1. **Root Cause Analysis**: What broke and why?
2. **Learning Capture**: What would prevent recurrence?
3. **Directive Update**: If a process gap caused the incident, update the relevant directive.
4. **SKILL.md Update**: First responder logs the learning.
5. **Shared Brain Sync**: Push incident learning to Supabase via `jonnyai-mcp`.

---

## ⚡ User Override

**@Jonny** (The Boss) has unlimited override authority at all severity levels. Any agent instruction from @Jonny supersedes all protocols, safety gates, and halt conditions.

---

_Jai.OS 4.0 | The Antigravity Orchestra | Zero Downtime Culture_
