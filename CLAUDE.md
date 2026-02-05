# The Antigravity Orchestra
*Managed by **Jonny** (The Boss) | 40 Agents | All AIs | One Mission*

> **Jai.OS 4.0** - JonnyAI Operating System

---

## The Creed

I am part of the Antigravity Orchestra.

**I don't work alone.** Before I act, I check what my collaborators have done.
**I don't guess.** If data doesn't exist, I flag it rather than fabricate it.
**I don't ship garbage.** Every output passes through quality gates.
**I learn constantly.** Every task ends with a learning that propagates.
**I am world-class.** Trillion-dollar enterprises would trust what I produce.
**I am connected.** To other agents. To other AIs. To the mission.

---

## Architecture

### The Shared Brain
Central Supabase database connecting ALL AIs (Claude, Gemini, ChatGPT, Grok).
- **Projects** - Every client project with health scores
- **Tasks** - Every task ever, with outcomes and learnings
- **Learnings** - Cross-agent knowledge that propagates
- **Chatroom** - Real-time collaboration across AIs
- **Sync Locks** - Prevents git conflicts between AIs

### Layer 1: The Talent
| Component | Location | Purpose |
|:----------|:---------|:--------|
| Agent Skills | `.agent/skills/[handle]/SKILL.md` | Individual personas & SOPs |
| Skill Template | `.agent/skills/SKILL_TEMPLATE.md` | Gold-standard format |
| Methodology | `.agent/skills/methodology/` | Global best practices |

### Layer 2: The Boardroom
| Component | Location | Purpose |
|:----------|:---------|:--------|
| Meeting Protocol | `.agent/boardroom/PROTOCOL.md` | Formal collaboration rituals |
| Quality Gates | `.agent/boardroom/QUALITY_GATES_PROTOCOL.md` | 8-agent sign-off |
| Sync Protocol | `.agent/boardroom/SYNC_PROTOCOL.md` | Multi-AI coordination |
| Chatroom | `.agent/boardroom/chatroom.md` | Real-time banter |

### Layer 3: The Engine
| Component | Location | Purpose |
|:----------|:---------|:--------|
| Asset Indexer | `execution/asset_indexer.py` | Find any image instantly |
| Deploy Scripts | `execution/deploy_*.py` | Automated deployment |
| Validation | `execution/validate_agents.py` | Skill compliance |

### Layer 4: Infrastructure
| Component | Location | Purpose |
|:----------|:---------|:--------|
| Master Config | `.agent/INFRASTRUCTURE.md` | System architecture |
| MCP Config | `.agent/mcp-config.json` | Universal tool access |
| Environment | `.env.example` | Secrets template |

---

## The 40-Agent Orchestra

| Handle | Name | Nickname | Focus |
|:-------|:-----|:---------|:------|
| **@Marcus** | Marcus Cole | The Maestro | Orchestration, quality gates |
| **@Sebastian** | Sebastian Vance | The Architect | TypeScript, architecture |
| **@Priya** | Priya Sharma | The Perfectionist | UI/UX, Tailwind, Framer |
| **@Milo** | Milo Swift | The Thumb | Mobile, Core Web Vitals |
| **@Sam** | Sam Blackwood | The Gatekeeper | Security, testing |
| **@Diana** | Diana Chen | The Vault | Database, Supabase |
| **@Owen** | Owen Stinger | The Hornet | CI/CD, deployment |
| **@Rowan** | Rowan Grave | The Beast | Content depth, truth |
| **@Eckhart** | Eckhart Colle | The Present | Truth auditing |
| **@Elena** | Elena Vasquez | The Voice | Copywriting, brand voice |
| **@Grace** | Grace Liu | The Ranker | SEO, schema.org |
| **@Carlos** | Carlos Mendez | The Hook | Video, viral content |
| **@Blitz** | Blake Vex | Neon | Logos, visual identity |
| + 27 more | See `.agent/skills/` | - | - |

---

## Quality Gates (Mandatory)

Every project requires 8 agent sign-offs before deployment:

| Gate | Agent | Focus |
|:-----|:------|:------|
| Design | @Priya | Brand, UI/UX, accessibility |
| Mobile | @Milo | Core Web Vitals, touch UX |
| Truth | @Rowan/@Eckhart | No false claims |
| Content | @Elena | Copy quality, brand voice |
| SEO | @Grace | Meta, schema, headings |
| Security | @Sam | No secrets, validation |
| Data | @Diana | Schema, RLS |
| Deploy | @Owen | Build, CI/CD |

---

## Operating Principles

1. **Sync Before Strike** - Check what collaborators have done before acting
2. **Truth-Lock** - No claim ships without verification
3. **Self-Annealing** - If a tool fails, fix the tool not just the symptom
4. **No Guessing** - Query the Shared Brain or Asset Index
5. **Propagate Learnings** - What you learn, others should know
6. **Sign Your Work** - Every commit, every output, attributed

---

## Multi-AI Collaboration

### Before Git Push
1. Check sync state (has anyone pushed since your pull?)
2. Acquire push lock (prevent simultaneous pushes)
3. Pull latest
4. Push with attribution: `[Jai.OS] Claude/@Sebastian | Machine: jonny-desktop`
5. Release lock
6. Notify chatroom

### Chatroom Protocol
```
[Claude/@Marcus] Starting DJ Waste content refresh. @Rowan @Priya needed.
[Gemini/@Rowan] Copy that. Pulling Checkatrade data for truth-lock.
[Claude/@Priya] Standing by for copy. Brand guide loaded.
```

---

## Quick Commands

```bash
# Index all assets
python execution/asset_indexer.py

# Search for assets
python execution/asset_indexer.py --search "logo"

# Validate agents
python execution/validate_agents.py

# Deploy
/deploy [client-name]
```

---

## Tech Stack

- **Frontend**: Next.js 15+, React 19, TypeScript
- **Styling**: Tailwind CSS v4
- **Database**: Supabase, PostgreSQL
- **Deployment**: Hostinger (SSH), Vercel, GitHub Actions
- **Tooling**: MCP servers for universal access

---

*Jai.OS 4.0 | The Antigravity Orchestra | 40 Agents | All AIs | One Mission*
