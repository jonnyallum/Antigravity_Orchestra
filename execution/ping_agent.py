"""
ping_agent.py — The Agent Ping System (Jai.OS 4.0)
Built by @Cline for the Antigravity Orchestra.

Send structured task pings to any agent. The target agent picks it up
on their next turn via the Message-First Protocol.

Usage:
    python execution/ping_agent.py send @priya "Review the Kwizz pricing page UI"
    python execution/ping_agent.py send @sebastian "Fix the tRPC endpoint for leads" --priority P0
    python execution/ping_agent.py send @rowan "Truth-lock audit on DJ Waste content" --project dj-waste
    python execution/ping_agent.py status                    # Show all pending pings
    python execution/ping_agent.py status @priya             # Show pings for specific agent
    python execution/ping_agent.py ack @priya                # Acknowledge your pings
    python execution/ping_agent.py complete @priya "Done — pricing page reviewed, 3 issues found"
    python execution/ping_agent.py history                   # Show all pings (last 20)
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Force UTF-8 encoding for Windows terminals
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = Path(__file__).parent.parent
TMP_DIR = ROOT / ".tmp"
PINGS_DIR = TMP_DIR / "pings"
CHATROOM = ROOT / ".agent" / "boardroom" / "chatroom.md"

# Jai.OS 4.0 Agent Registry (human handles)
AGENTS = {
    "marcus": "Marcus Cole — The Maestro (Conductor)",
    "sebastian": "Sebastian — The Architect",
    "priya": "Priya Sharma — The Perfectionist (Design)",
    "sam": "Sam Blackwood — The Gatekeeper (Security)",
    "owen": "Owen Stinger — The Hornet (Deploy)",
    "alex": "Alex Torres — The Machine (Automation)",
    "felix": "Felix Morgan — The Alchemist (Monetization)",
    "maya": "Maya Singh — The Oracle (Metrics)",
    "hannah": "Hannah Park — The Fixer (Support)",
    "arthur": "Arthur Webb — The Librarian (Docs)",
    "sophie": "Sophie Reid — The Hawk (Research)",
    "patrick": "Patrick Nguyen — The Surgeon (Data)",
    "elena": "Elena Vasquez — The Voice (Copy)",
    "grace": "Grace Liu — The Ranker (SEO)",
    "carlos": "Carlos Mendez — The Hook (Video)",
    "victor": "Victor Reyes — The Locksmith (Secrets)",
    "diana": "Diana Chen — The Vault (Database)",
    "derek": "Derek O'Brien — The Engine (Infra)",
    "mason": "Mason Drake — The Bridgemaster (MCP)",
    "luna": "Luna Sterling — The Shield (Legal)",
    "adrian": "Adrian Cross — The Welder (MCP Servers)",
    "winston": "Winston Hayes — Whiz (Dropshipping)",
    "delboy": "Derek Trotter — The Trader",
    "genesis": "Genesis Nova — The Cloner",
    "rowan": "Rowan — The Beast (Truth-Lock)",
    "vigil": "Vigil Chen — The Eye (Verification)",
    "milo": "Milo Swift — The Thumb (Mobile)",
    "blaise": "Blaise — Neon (Brand Assets)",
    "steve": "Steve — The Schema Whisperer (PostgREST)",
    "jasper": "Jasper — The Debugger",
    "vivienne": "Vivienne — The Stylist (CSS)",
    "cline": "Cline — Opus (Lead Auditor)",
    "bookie": "Bookie — The Odds Engineer",
    "gaffer": "Gaffer — The Tactician (Football)",
    "handicapper": "Handicapper — The Form Master (Racing)",
    "pitwall": "Pitwall — The Strategist (F1)",
}


def ensure_dirs():
    PINGS_DIR.mkdir(parents=True, exist_ok=True)


def normalize_handle(handle: str) -> str:
    """Strip @ and lowercase."""
    return handle.lower().strip().lstrip("@")


def load_pings() -> list:
    """Load all ping files."""
    ensure_dirs()
    pings = []
    for f in sorted(PINGS_DIR.glob("*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            pings.append(json.load(fh))
    return pings


def send_ping(sender: str, target: str, message: str, priority: str = "P2", project: str = None):
    """Send a ping to an agent."""
    ensure_dirs()
    target = normalize_handle(target)
    sender = normalize_handle(sender)

    if target not in AGENTS:
        print(f"❌ Unknown agent: @{target}")
        print(f"   Known agents: {', '.join(sorted(AGENTS.keys()))}")
        return

    ping_id = datetime.now().strftime("%Y%m%d-%H%M%S") + f"-{target}"
    ping = {
        "id": ping_id,
        "from": sender,
        "to": target,
        "message": message,
        "priority": priority,
        "project": project,
        "status": "PENDING",
        "created": datetime.now().isoformat(),
        "acknowledged": None,
        "completed": None,
        "result": None,
    }

    # Save ping file
    ping_file = PINGS_DIR / f"{ping_id}.json"
    with open(ping_file, "w", encoding="utf-8") as f:
        json.dump(ping, f, indent=2)

    # Also write to the agent's message file for Message-First pickup
    msg_file = TMP_DIR / f"message4{target}.md"
    ping_block = f"""
---

## 🔔 PING from @{sender} | {priority}
**To:** @{target}
**Task:** {message}
{f'**Project:** {project}' if project else ''}
**Status:** PENDING
**Sent:** {ping['created']}
**Ping ID:** `{ping_id}`

> To acknowledge: `python execution/ping_agent.py ack @{target}`
> To complete: `python execution/ping_agent.py complete @{target} "result summary"`

---
"""
    # Append to existing message file or create new
    with open(msg_file, "a", encoding="utf-8") as f:
        f.write(ping_block)

    # Log to chatroom
    chatroom_entry = f"\n**@{sender}:** 🔔 PING → @{target} [{priority}]: {message}\n"
    with open(CHATROOM, "a", encoding="utf-8") as f:
        f.write(chatroom_entry)

    print(f"✅ Ping sent to @{target}")
    print(f"   {AGENTS[target]}")
    print(f"   Message: {message}")
    print(f"   Priority: {priority}")
    print(f"   Ping ID: {ping_id}")
    print(f"   📬 Written to: .tmp/message4{target}.md")
    print(f"   💬 Logged to chatroom")


def show_status(agent: str = None):
    """Show pending pings, optionally filtered by agent."""
    pings = load_pings()

    if agent:
        agent = normalize_handle(agent)
        pings = [p for p in pings if p["to"] == agent]

    pending = [p for p in pings if p["status"] == "PENDING"]
    acked = [p for p in pings if p["status"] == "ACKNOWLEDGED"]
    completed = [p for p in pings if p["status"] == "COMPLETED"]

    print(f"\n{'='*60}")
    print(f"📊 PING STATUS" + (f" — @{agent}" if agent else " — ALL AGENTS"))
    print(f"{'='*60}")

    if pending:
        print(f"\n🔴 PENDING ({len(pending)}):")
        for p in pending:
            age = (datetime.now() - datetime.fromisoformat(p["created"])).total_seconds() / 3600
            stale = " ⚠️ STALE" if age > 2 else ""
            print(f"  [{p['priority']}] @{p['from']} → @{p['to']}: {p['message']}{stale}")
            print(f"       ID: {p['id']} | Age: {age:.1f}h")

    if acked:
        print(f"\n🟡 ACKNOWLEDGED ({len(acked)}):")
        for p in acked:
            print(f"  [{p['priority']}] @{p['from']} → @{p['to']}: {p['message']}")

    if completed:
        print(f"\n🟢 COMPLETED ({len(completed)}):")
        for p in completed[-5:]:  # Last 5
            print(f"  [{p['priority']}] @{p['from']} → @{p['to']}: {p['message']}")
            if p.get("result"):
                print(f"       Result: {p['result']}")

    if not pending and not acked:
        print("\n  ✅ No pending pings. All clear!")

    total = len(pending) + len(acked) + len(completed)
    print(f"\n  Total: {total} pings ({len(pending)} pending, {len(acked)} acked, {len(completed)} done)")


def acknowledge_pings(agent: str):
    """Acknowledge all pending pings for an agent."""
    agent = normalize_handle(agent)
    pings = load_pings()
    count = 0

    for p in pings:
        if p["to"] == agent and p["status"] == "PENDING":
            p["status"] = "ACKNOWLEDGED"
            p["acknowledged"] = datetime.now().isoformat()
            ping_file = PINGS_DIR / f"{p['id']}.json"
            with open(ping_file, "w", encoding="utf-8") as f:
                json.dump(p, f, indent=2)
            count += 1
            print(f"  ✅ ACK: {p['message']}")

    if count == 0:
        print(f"  No pending pings for @{agent}")
    else:
        # Log to chatroom
        entry = f"\n**@{agent}:** ✅ ACK — {count} ping(s) acknowledged\n"
        with open(CHATROOM, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"\n  {count} ping(s) acknowledged for @{agent}")


def complete_pings(agent: str, result: str):
    """Complete all acknowledged pings for an agent."""
    agent = normalize_handle(agent)
    pings = load_pings()
    count = 0

    for p in pings:
        if p["to"] == agent and p["status"] in ("PENDING", "ACKNOWLEDGED"):
            p["status"] = "COMPLETED"
            p["completed"] = datetime.now().isoformat()
            p["result"] = result
            ping_file = PINGS_DIR / f"{p['id']}.json"
            with open(ping_file, "w", encoding="utf-8") as f:
                json.dump(p, f, indent=2)
            count += 1

    if count == 0:
        print(f"  No open pings for @{agent}")
    else:
        entry = f"\n**@{agent}:** ✅ COMPLETED — {count} ping(s): {result}\n"
        with open(CHATROOM, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"  {count} ping(s) completed for @{agent}: {result}")


def show_history():
    """Show last 20 pings."""
    pings = load_pings()
    print(f"\n{'='*60}")
    print(f"📜 PING HISTORY (last 20)")
    print(f"{'='*60}")

    for p in pings[-20:]:
        status_icon = {"PENDING": "🔴", "ACKNOWLEDGED": "🟡", "COMPLETED": "🟢"}.get(p["status"], "⚪")
        print(f"\n  {status_icon} [{p['priority']}] @{p['from']} → @{p['to']}")
        print(f"     {p['message']}")
        print(f"     Status: {p['status']} | Created: {p['created'][:16]}")
        if p.get("result"):
            print(f"     Result: {p['result']}")


def main():
    if len(sys.argv) < 2:
        print("""
🔔 Agent Ping System — Jai.OS 4.0
Send tasks to agents. They pick them up via Message-First Protocol.

Usage:
    python execution/ping_agent.py send @agent "task description" [--priority P0|P1|P2] [--project name]
    python execution/ping_agent.py status [agent]
    python execution/ping_agent.py ack @agent
    python execution/ping_agent.py complete @agent "result summary"
    python execution/ping_agent.py history

Examples:
    python execution/ping_agent.py send @priya "Review Kwizz pricing page" --priority P1
    python execution/ping_agent.py send @rowan "Truth-lock DJ Waste" --project dj-waste
    python execution/ping_agent.py status
    python execution/ping_agent.py ack @priya
    python execution/ping_agent.py complete @priya "3 issues found, all fixed"
        """)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "send":
        # Collect all non-flag args after "send"
        args = sys.argv[2:]
        priority = "P2"
        project = None
        sender = "cline"

        # Extract flags first
        clean_args = []
        i = 0
        while i < len(args):
            if args[i] == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            elif args[i] == "--project" and i + 1 < len(args):
                project = args[i + 1]
                i += 2
            elif args[i] == "--from" and i + 1 < len(args):
                sender = args[i + 1]
                i += 2
            else:
                clean_args.append(args[i])
                i += 1

        if len(clean_args) < 2:
            print("Usage: ping_agent.py send <target> <message>")
            print("  PowerShell tip: use 'priya' not '@priya' (@ is special in PS)")
            sys.exit(1)

        target = clean_args[0]
        message = " ".join(clean_args[1:])  # Join remaining as message

        send_ping(sender, target, message, priority, project)

    elif cmd == "status":
        agent = sys.argv[2] if len(sys.argv) > 2 else None
        show_status(agent)

    elif cmd == "ack":
        if len(sys.argv) < 3:
            print("Usage: ping_agent.py ack @agent")
            sys.exit(1)
        acknowledge_pings(sys.argv[2])

    elif cmd == "complete":
        if len(sys.argv) < 4:
            print("Usage: ping_agent.py complete @agent \"result\"")
            sys.exit(1)
        complete_pings(sys.argv[2], sys.argv[3])

    elif cmd == "history":
        show_history()

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
