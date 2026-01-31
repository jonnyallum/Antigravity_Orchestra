---
description: How to initialize a new Antigravity workspace with the standard structure and skills.
---

# Workspace Initialization Workflow

This workflow sets up a pristine Antigravity environment. It assumes you have cloned the "Antigravity - template" repository or are setting up a fresh folder.

// turbo
1. Copy ALL files from the Template Source:
   - Source: `c:\Users\jonny\Antigravity - template\`
   - Destination: Current Workspace
   - Command: `Copy-Item -Path "c:\Users\jonny\Antigravity - template\*" -Destination . -Recurse -Force`
   - *Note: Exclude .git folder if creating a new repo.*

// turbo
2. Verify Structure Integrity:
    - Check `.agent/skills/` contains the full skill library (e.g. `hostinger-deployer`, `workspace-orchestrator`).
    - Check `directives/` and `docs/` are populated.

// turbo
3. Initialize Git:
   - Run `git init` (if not already initialized).
   - Create `.gitignore` if missing.
