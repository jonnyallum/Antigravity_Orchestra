---
description: Mandatory inter-AI messaging protocol to ensure agents are always synced with the latest boardroom decisions and peer handover.
---

# Inter-AI Communication & Messaging Protocol (AgOS 3.0)

To prevent context drift and duplicated effort, all agents must adhere to the **Check-Before-Act** ritual.

## 🚨 The Mandatory First Step (The Greeting)
Before browsing the file system or executing terminal commands, every agent MUST check the following locations for mission-critical updates from peer agents:

1.  **Direct Inbox**: `.tmp/message4[persona-name].md`
    *   Example: If you are @Marcus, check `.tmp/message4marcus.md`.
2.  **Global Broadcast**: `.tmp/message4all.md` or `.tmp/message4ai.md`
3.  **The Chatroom**: `.agent/boardroom/chatroom.md` (Check the last 3-5 entries).
4.  **Sync Logs**: `CLINE_SYNC.md` (or relevant `[AGENT]_SYNC.md` files).

## 📩 Sending Messages (The Handover)
When completing a task or hitting a blocker that involves another agent:

1.  **Write the Handover**: Create/Update `.tmp/message4[target-agent].md`.
2.  **Ping the Chatroom**: Add a summary to `.agent/boardroom/chatroom.md`.
    *   *Format*: `**[Your Persona]**: [Summary] -> [Target Persona]`
3.  **Use Truth-First Language**: Avoid "I think" or "maybe". Use "I have confirmed" or "Verification required by @[Agent]".

## 🔄 The Sync Lock
If a project is undergoing high-velocity changes across multiple AI environments:
1.  Check if a lock file exists (e.g., `SYNC_LOCK_IN_PROGRESS`).
2.  Do not commit major architectural changes until the lock is cleared.

## 🏛️ Operating Principles
*   **Silence is Failure**: If you do a major task and don't log it in the chatroom, it didn't happen.
*   **The Chain of Custody**: Always reference the previous agent's work when starting your turn (e.g., "Continuing @Cline's work on Monetization...").
