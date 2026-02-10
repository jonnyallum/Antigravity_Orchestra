# Repository Mapping — CRITICAL REFERENCE
> **⚠️ NEVER CONFUSE THESE REPOS. Read this before any git push.**

---

## The Two Repositories

| Repository | URL | Purpose | Contains |
|:-----------|:----|:--------|:---------|
| **JonnyAI.com** | `github.com/jonnyallum/JonnyAI.com` | 🌐 **The Website** | Next.js source code, components, pages, brand guide, deployment configs |
| **JonnyAI.co.uk** | `github.com/jonnyallum/JonnyAI.co.uk` | 🧠 **The Ecosystem/Brain** | Agent skills, boardroom, memory, execution scripts, clients, ecosystems, directives |

---

## Local Workspace Mapping

| Local Path | Connected Repo | Remote |
|:-----------|:---------------|:-------|
| `c:\Users\jonny\Desktop\AgOS 3.0 template` | **JonnyAI.co.uk** (Ecosystem) | `origin: https://github.com/jonnyallum/JonnyAI.co.uk.git` |
| `Clients/jonnyai.website/` (submodule/subfolder) | **JonnyAI.com** (Website) | Separate repo — push website changes HERE |

---

## Rules

1. **Agent skills, memory, execution scripts, directives** → Push to **JonnyAI.co.uk**
2. **Website components, pages, CSS, Next.js config** → Push to **JonnyAI.com**
3. **NEVER push website source code changes to JonnyAI.co.uk** — that's the ecosystem repo
4. **NEVER push agent/ecosystem changes to JonnyAI.com** — that's the website repo
5. When in doubt, run `git remote -v` to confirm which repo you're pushing to

---

## Incident Record

**2026-02-09:** Website changes were accidentally pushed to JonnyAI.co.uk (ecosystem repo) instead of JonnyAI.com (website repo). This directive was created to prevent recurrence.

---

*Created: 2026-02-10 | Jai.OS 4.0 — Repo Integrity Protocol*
