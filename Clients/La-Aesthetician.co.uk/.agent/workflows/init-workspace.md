---
description: How to initialize a new Antigravity workspace with the standard structure and skills.
---

# Workspace Initialization Workflow

This workflow sets up a pristine Antigravity environment. It assumes you have cloned the "Antigravity - template" repository or are setting up a fresh folder.

// turbo
1. Create the standard directory structure:
    - `.agent/skills` for capabilities
    - `docs` for documentation
    - `directives` for SOPs
    - `execution` for scripts
    - `.tmp` for intermediate files

// turbo
2. Ensure the essential documentation exists:
    - `README.md` (Entry point)
    - `docs/WORKSPACE_GUIDE.md` (Operating manual)
    - `docs/SKILL_CATALOG.md` (Registry of skills)

// turbo
3. Verify the `workspace-orchestrator` skill is present in `.agent/skills/workspace-orchestrator/SKILL.md`.

// turbo
4. (Optional) Run `git init` if not already a repo.
