---
description: Typed artifact standards for all Antigravity deliverables. Ensures every output is verifiable, auditable, and reusable.
---

# Artifact Standards (Jai.OS 4.0)

Every agent output must be a **typed, verifiable artifact**. No undocumented work.

---

## 📁 Artifact Locations

| Type               | Location                         | Persistence                              |
| :----------------- | :------------------------------- | :--------------------------------------- |
| **Intermediates**  | `.tmp/`                          | Ephemeral — regenerable, never committed |
| **Task Artifacts** | `.tmp/[task-id]/`                | Per-task working directory               |
| **Deliverables**   | GitHub, Supabase, deployed sites | Permanent — user-visible                 |
| **Reports**        | `.tmp/reports/`                  | Sprint-scoped, archived quarterly        |
| **Screenshots**    | `.tmp/screenshots/`              | Visual verification evidence             |

---

## 🏷️ Artifact Types

### Code Artifacts

- **Format**: `.ts`, `.tsx`, `.py`, `.css`, `.json`
- **Standard**: Must pass lint + build before marking GATE_CLEARED
- **Owner**: Dev Tier agents (@Sebastian, @Adrian, @Owen, @Derek)

### Design Artifacts

- **Format**: `.figma` (link), `.png`, `.svg`, `.webp`
- **Standard**: Must include responsive variants (desktop + mobile)
- **Owner**: Design Tier agents (@Priya, @Blaise, @Vivienne)

### Documentation Artifacts

- **Format**: `.md`
- **Standard**: Must include frontmatter (`title`, `date`, `author`)
- **Owner**: @Arthur, @Elena, any agent documenting work

### Data Artifacts

- **Format**: `.json`, `.csv`, `.sql`
- **Standard**: Must include schema description or header row
- **Owner**: @Diana, @Steve, @Patrick, @Nina

### Media Artifacts

- **Format**: `.mp4`, `.webm`, `.webp`
- **Standard**: Must include dimensions, duration, and purpose
- **Owner**: @Carlos, @Blaise

### Verification Artifacts

- **Format**: `.md` (verdicts), `.json` (test results), `.png` (screenshots)
- **Standard**: Must reference the artifact being verified
- **Owner**: @Vigil, @Sam, @Rowan

### Course Artifacts

- **Format**: `.md` (blueprints, lesson specs), `.pdf` (worksheets), `.json` (quiz data)
- **Standard**: Must link to parent blueprint
- **Owner**: @Coursewright

---

## ✅ Artifact Checklist (Before GATE_CLEARED)

Every artifact must pass:

1. **Exists**: File is present at the `PAYLOAD_PATH` referenced in the State Packet.
2. **Typed**: File extension matches the expected artifact type.
3. **Attributed**: Contains author handle or is traceable to a TASK_ID.
4. **Verifiable**: Can be independently validated (builds, renders, opens correctly).
5. **Non-placeholder**: Contains real content — no Lorem ipsum, no "TODO", no empty shells.

---

## 🚫 Anti-Patterns

- ❌ Committing `.tmp/` files to GitHub
- ❌ Artifacts without a parent TASK_ID
- ❌ Screenshots without context (what page, what state, what was being verified)
- ❌ JSON files without schema documentation
- ❌ "I'll finish this later" stubs pushed as deliverables

---

_Jai.OS 4.0 | The Antigravity Orchestra | Verifiable Outputs Only_
