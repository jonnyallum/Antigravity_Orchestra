# Repository Mapping — CRITICAL REFERENCE
> **⚠️ NEVER CONFUSE THESE REPOS. Read this before any git push.**

---

## The Two Repositories

| Repository | URL | Purpose | Contains |
|:-----------|:----|:--------|:---------|
| **jonnyai_website** | `github.com/jonnyallum/jonnyai_website` | 🌐 **The Website** | Next.js source code, components, pages, brand guide, deployment configs |
| **Antigravity_Orchestra** | `github.com/jonnyallum/Antigravity_Orchestra` | 🧠 **The Orchestra/Brain** | Agent skills, boardroom, memory, execution scripts, clients, ecosystems, directives |

---

## Local Workspace Mapping

| Local Path | Connected Repo | Remote |
|:-----------|:---------------|:-------|
| `c:\Users\jonny\Desktop\AgOS 3.0 template` | **Antigravity_Orchestra** (Orchestra) | `origin: https://github.com/jonnyallum/Antigravity_Orchestra.git` |
| `Clients/jonnyai.website/` (subfolder) | **jonnyai_website** (Website) | Separate repo — push website changes HERE |

---

## Rules

1. **Agent skills, memory, execution scripts, directives** → Push to **Antigravity_Orchestra**
2. **Website components, pages, CSS, Next.js config** → Push to **jonnyai_website**
3. **NEVER push website source code changes to Antigravity_Orchestra** — that's the orchestra repo
4. **NEVER push agent/orchestra changes to jonnyai_website** — that's the website repo
5. When in doubt, run `git remote -v` to confirm which repo you're pushing to

---

## Rename History

| Date | Old Name | New Name | Reason |
|:-----|:---------|:---------|:-------|
| 2026-02-11 | `JonnyAI.co.uk` | `Antigravity_Orchestra` | Clarity — name reflects purpose |
| 2026-02-11 | `JonnyAI.com` | `jonnyai_website` | Clarity — name reflects purpose |

## Incident Record

**2026-02-09:** Website changes were accidentally pushed to the ecosystem repo instead of the website repo. This directive was created to prevent recurrence.

---

*Created: 2026-02-10 | Updated: 2026-02-11 (repo rename) | Jai.OS 4.0 — Repo Integrity Protocol*
