---
description: Run the full AgOS 3.0 Brain Sync Protocol to align all agents and save progress.
---
# /sync - Brain Sync Protocol

This workflow executes the complete synchronization cycle to ensure the local workspace, the Shared Brain (Supabase), and the public website are all in perfect alignment.

// turbo-all
1. Validate agent SKILL.md structures.
2. Generate and store session reports.
3. Push agent learnings to the Shared Brain.
4. Stage, commit, and push all code changes to GitHub.
5. Update the public roster on jonnyai.website.
6. Broadcast sync status to the Agency Chatroom.
7. Clean up redundant files (cache, ghost files, stale temp artifacts).

```bash
python execution/brain_sync_protocol.py
```

### Purpose
- **Alignment**: Brings all specialists and infrastructure into synchronized state.
- **Persistence**: Ensures no learning or progress is lost if the environment resets.
- **Readiness**: Clears the literal and figurative desk for the next mission.
