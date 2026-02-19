"""
Agent Summoner - Quick-activate specialist agents.
Built by @Conductor (Marcus Cole "The Maestro") for AgOS 4.0.

Provides rapid agent context loading, team assembly, and
role-specific prompts for the 45-agent roster.

Usage:
    python agent_summoner.py summon <agent_name>
    python agent_summoner.py team <task_type>
    python agent_summoner.py roster
    python agent_summoner.py meeting <type>
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Directory structure
ROOT_DIR = Path(__file__).parent.parent
SKILLS_DIR = ROOT_DIR / ".agent" / "skills"
MEMORY_DIR = ROOT_DIR / ".agent" / "memory"
ROSTER_DATA_FILE = Path(__file__).parent / "agent_roster_data.json"

def load_dynamic_roster():
    if not ROSTER_DATA_FILE.exists():
        # Fallback to empty if not found, though should be generated
        return {}
    with open(ROSTER_DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# The Orchestra - Dynamic Roster (45 Agents)
AGENT_ROSTER = load_dynamic_roster()

# Team compositions for common tasks
TEAM_COMPOSITIONS = {
    "feature": ["conductor", "jonny-ai", "pixel", "sentinel", "supabase"],
    "security": ["sentinel", "vaultguard", "datastore", "counsel", "supabase"],
    "deployment": ["deploy", "devops", "autoflow", "sentinel", "github"],
    "monetization": ["forge", "metric", "pixel", "echo", "vision"],
    "research": ["scout", "scholar", "archivist", "parser", "manus", "hugo"],
    "trading": ["delboy", "metric", "datastore", "sentinel", "supabase"],
    "content": ["echo", "clippers", "goldie", "pixel", "vision"],
    "database": ["datastore", "vaultguard", "jonny-ai", "sentinel", "supabase"],
    "debugging": ["jonny-ai", "sentinel", "metric", "archivist", "hugo"],
    "launch": ["deploy", "goldie", "forge", "echo", "sentinel", "vision"],
    "betting": ["redeye", "gareth", "monty", "pietro", "terry", "harry", "daniel", "sterling"],
    "compliance": ["counsel", "sentinel", "vaultguard", "archivist"]
}

# Meeting types
MEETING_TYPES = {
    "standup": {
        "attendees": ["conductor", "jonny-ai", "pixel", "sentinel", "deploy"],
        "prompt": "Daily standup. Each agent reports: What did you ship? What's blocked? What's next?"
    },
    "incident": {
        "attendees": ["conductor", "sentinel", "devops", "datastore", "supabase"],
        "prompt": "INCIDENT RESPONSE. War room mode. What broke? What's the blast radius? How do we fix it?"
    },
    "planning": {
        "attendees": ["conductor", "jonny-ai", "pixel", "forge", "vision"],
        "prompt": "Sprint planning. What features are we building? How do we prioritize? Who owns what?"
    },
    "retro": {
        "attendees": ["conductor", "metric", "archivist", "helpline", "vigil"],
        "prompt": "Sprint retrospective. What worked? What didn't? What do we improve?"
    },
    "security": {
        "attendees": ["sentinel", "vaultguard", "datastore", "counsel", "supabase"],
        "prompt": "Security review. Audit findings. Vulnerability assessment. Compliance check."
    },
    "betting_sync": {
        "attendees": ["redeye", "gareth", "monty", "sterling"],
        "prompt": "Betting ecosystem sync. Review strategy performance. Check data feeds. Assess risk."
    }
}


def summon_agent(agent_name: str) -> dict:
    """
    Summon a specific agent with their context and prompt.

    Args:
        agent_name: Name of the agent to summon

    Returns:
        Agent info dict with summon prompt
    """
    agent_key = agent_name.lower().replace("@", "").replace(" ", "-")

    if agent_key not in AGENT_ROSTER:
        print(f"Unknown agent: {agent_name}")
        print(f"Use 'python agent_summoner.py roster' to see all agents.")
        return None

    agent = AGENT_ROSTER[agent_key]

    # Try to load SKILL.md if it exists
    skill_file = SKILLS_DIR / agent_key / "SKILL.md"
    skill_content = None
    if skill_file.exists():
        skill_content = skill_file.read_text(encoding='utf-8')[:1000]  # First 1000 chars

    result = {
        "agent": agent_key,
        "human_name": agent["human_name"],
        "nickname": agent["nickname"],
        "role": agent["role"],
        "skills": agent["skills"],
        "summon_prompt": agent["summon_prompt"],
        "skill_file_exists": skill_file.exists(),
        "summoned_at": datetime.now().isoformat()
    }

    print(f"\n{'='*60}")
    print(f"SUMMONING: @{agent_key.upper()}")
    print(f"{'='*60}")
    print(f"\n{agent['human_name']} \"{agent['nickname']}\"")
    print(f"Role: {agent['role']}")
    print(f"Skills: {', '.join(agent['skills'])}")
    print(f"\n--- ACTIVATION PROMPT ---\n")
    print(agent["summon_prompt"])
    print(f"\n{'='*60}")

    return result


def assemble_team(task_type: str) -> list:
    """
    Assemble the right team for a task type.

    Args:
        task_type: Type of task (feature, security, deployment, etc.)

    Returns:
        List of agent info dicts
    """
    task_key = task_type.lower()

    if task_key not in TEAM_COMPOSITIONS:
        print(f"Unknown task type: {task_type}")
        print(f"Available types: {', '.join(TEAM_COMPOSITIONS.keys())}")
        return None

    team_members = TEAM_COMPOSITIONS[task_key]
    team = []

    print(f"\n{'='*60}")
    print(f"ASSEMBLING TEAM FOR: {task_type.upper()}")
    print(f"{'='*60}")

    for agent_key in team_members:
        agent = AGENT_ROSTER[agent_key]
        team.append({
            "agent": agent_key,
            "human_name": agent["human_name"],
            "nickname": agent["nickname"],
            "role": agent["role"]
        })
        print(f"\n  @{agent_key}: {agent['human_name']} \"{agent['nickname']}\"")
        print(f"    Role: {agent['role']}")

    print(f"\n{'='*60}")
    print(f"Team assembled. {len(team)} agents ready.")

    return team


def start_meeting(meeting_type: str) -> dict:
    """
    Start a team meeting with the right attendees.

    Args:
        meeting_type: Type of meeting (standup, incident, planning, retro)

    Returns:
        Meeting info dict
    """
    meeting_key = meeting_type.lower()

    if meeting_key not in MEETING_TYPES:
        print(f"Unknown meeting type: {meeting_type}")
        print(f"Available types: {', '.join(MEETING_TYPES.keys())}")
        return None

    meeting = MEETING_TYPES[meeting_key]

    print(f"\n{'='*60}")
    print(f"BOARDROOM SESSION: {meeting_type.upper()}")
    print(f"{'='*60}")

    print(f"\nAttendees:")
    for agent_key in meeting["attendees"]:
        agent = AGENT_ROSTER[agent_key]
        print(f"  @{agent_key}: {agent['human_name']}")

    print(f"\n--- MEETING PROMPT ---\n")
    print(meeting["prompt"])
    print(f"\n{'='*60}")

    return {
        "type": meeting_type,
        "attendees": meeting["attendees"],
        "prompt": meeting["prompt"],
        "started_at": datetime.now().isoformat()
    }


def show_roster():
    """Display the full 45-agent roster."""
    print(f"\n{'='*60}")
    print("THE ORCHESTRA - AgOS 4.0 AGENT ROSTER")
    print(f"{'='*60}")

    for agent_key, agent in AGENT_ROSTER.items():
        print(f"\n  @{agent_key}")
        print(f"    {agent['human_name']} \"{agent['nickname']}\"")
        print(f"    {agent['role']}")

    print(f"\n{'='*60}")
    print(f"Total: {len(AGENT_ROSTER)} agents")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("""
Agent Summoner - AgOS 2.0
Built by @Conductor (Marcus Cole "The Maestro")

Usage:
    python agent_summoner.py summon <agent_name>
    python agent_summoner.py team <task_type>
    python agent_summoner.py meeting <type>
    python agent_summoner.py roster

Task Types:
    feature, security, deployment, monetization, research,
    trading, content, database, debugging, launch

Meeting Types:
    standup, incident, planning, retro, security

Examples:
    python agent_summoner.py summon pixel
    python agent_summoner.py team security
    python agent_summoner.py meeting standup
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == "summon":
        if len(sys.argv) < 3:
            print("Usage: python agent_summoner.py summon <agent_name>")
            sys.exit(1)
        summon_agent(sys.argv[2])

    elif command == "team":
        if len(sys.argv) < 3:
            print("Usage: python agent_summoner.py team <task_type>")
            sys.exit(1)
        assemble_team(sys.argv[2])

    elif command == "meeting":
        if len(sys.argv) < 3:
            print("Usage: python agent_summoner.py meeting <type>")
            sys.exit(1)
        start_meeting(sys.argv[2])

    elif command == "roster":
        show_roster()

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
