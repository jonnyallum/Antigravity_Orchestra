---
description: Mandatory inter-AI messaging protocol to ensure agents are always synced with the latest boardroom decisions and peer handover.
---

# Inter-AI Communication & Messaging Protocol (Jai.OS 4.0)

To prevent context drift and duplicated effort, all agents must adhere to the **Check-Before-Act** ritual.

## 🚨 The Mandatory First Step (The Greeting)
Before browsing the file system or executing terminal commands, every agent MUST check the following locations for mission-critical updates from peer agents:

1.  **Direct Inbox**: `.tmp/message4[persona-name].md`
    *   Example: If you are @Marcus, check `.tmp/message4marcus.md`.
2.  **Global Broadcast**: `.tmp/message4all.md` or `.tmp/message4ai.md`
3.  **The Chatroom**: `.agent/boardroom/chatroom.md` (Check the last 3-5 entries).
4.  **Sync Logs**: `CLINE_SYNC.md` (or relevant `[AGENT]_SYNC.md` files).

## ✉️ Sending Messages (The Handover)
When completing a task or hitting a blocker that involves another agent:

1.  **Write the Handover**: Create/Update `.tmp/message4[target-agent].md`.
2.  **Ping the Chatroom**: Add a summary to `.agent/boardroom/chatroom.md`.
    *   *Format*: `**[Your Persona]**: [Summary] -> [Target Persona]`
3.  **Use Truth-First Language**: Avoid "I think" or "maybe". Use "I have confirmed" or "Verification required by @[Agent]".

## 🛠️ Shell & Tool Compliance (Windows First)
To avoid agent execution loops and syntax failures:

1.  **PowerShell Chaining**: Always use `;` to chain commands. Never use `&` or `&&` in the terminal unless verified for the current shell.
2.  **Tool Schema Verification**: If a tool call fails with a "missing parameter" error, immediately re-read your tool definitions (e.g., `list_tools`). **Do not guess parameter names.**
3.  **Pathing**: Use absolute paths for all file operations to prevent "File Not Found" errors during cross-environment sync.

## 🔄 The Sync Lock
If a project is undergoing high-velocity changes across multiple AI environments:
1.  Check if a lock file exists (e.g., `SYNC_LOCK_IN_PROGRESS`).
2.  Do not commit major architectural changes until the lock is cleared.

## ✅ Acknowledgment Protocol (New: 2026-02-07)

Messages without acknowledgment are messages that were never received. Every handover requires a closed loop.

### Sending Agent Responsibilities
1. Write the message to `.tmp/message4[target].md`
2. Post summary to chatroom
3. **Set a status flag** at the bottom of the message:
   ```
   ---
   STATUS: AWAITING_ACK
   SENT: YYYY-MM-DD HH:MM UTC
   SENDER: @[YourHandle]
   ```

### Receiving Agent Responsibilities
1. Read the message as first action (Message-First Protocol)
2. **Acknowledge receipt** by updating the status:
   ```
   ---
   STATUS: ACKNOWLEDGED
   ACKED: YYYY-MM-DD HH:MM UTC
   RECEIVER: @[YourHandle]
   ACTION: [Brief description of what you'll do]
   ```
3. Post acknowledgment to chatroom: `"@[You]: ACK from @[Sender] — [action summary]"`

### Completion
When the requested work is done:
```
---
STATUS: COMPLETED
COMPLETED: YYYY-MM-DD HH:MM UTC
RECEIVER: @[YourHandle]
RESULT: [Brief outcome]
```

### Stale Messages
If a message has `STATUS: AWAITING_ACK` for >2 hours, @Marcus should escalate.

## 📊 Feedback Engine Integration (New: 2026-02-07)

Every significant task completion should be logged to the feedback engine:

```bash
python execution/feedback_engine.py log [agent] [task-type] [true/false] --learning="[what was learned]"
```

This is **not optional**. The feedback engine is the only way the system learns at scale. If you complete a task and don't log it, the system doesn't improve.

### When to Log
- After every deployment
- After every incident resolution
- After every Team Talk
- After every quality gate review
- After any task that took >30 minutes

## 🏛️ Operating Principles
*   **Silence is Failure**: If you do a major task and don't log it in the chatroom, it didn't happen.
*   **The Chain of Custody**: Always reference the previous agent's work when starting your turn (e.g., "Continuing @Cline's work on Monetization...").
*   **Closed Loops Only**: Every message sent must be acknowledged. Every task completed must be logged. No open threads.
*   **Feedback is Fuel**: The feedback engine is the nervous system. Feed it or the system stays blind.
