"""
Feedback Engine - Processes task outcomes and extracts learnings.
Part of the AgOS 2.0 Feedback Loop System.

Usage:
    python feedback_engine.py log <agent> <task_type> <success> [options]
    python feedback_engine.py health <agent>
    python feedback_engine.py gaps
    python feedback_engine.py report
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Directory structure
AGENT_DIR = Path(__file__).parent.parent / ".agent"
MEMORY_DIR = AGENT_DIR / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
INCIDENTS_DIR = MEMORY_DIR / "incidents"
HEALTH_FILE = MEMORY_DIR / "agent-health.json"


def ensure_directories():
    """Create necessary directories if they don't exist."""
    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    INCIDENTS_DIR.mkdir(parents=True, exist_ok=True)


def log_task_outcome(
    agent: str,
    task_type: str,
    success: bool,
    duration_minutes: int = 0,
    blockers: list = None,
    human_intervention: bool = False,
    learnings: list = None
) -> dict:
    """
    Log the outcome of a completed task for feedback analysis.

    Args:
        agent: Name of the agent (e.g., 'jonny-ai')
        task_type: Category of task (e.g., 'feature', 'bugfix', 'review')
        success: Whether the task was successful
        duration_minutes: How long the task took
        blockers: List of blockers encountered
        human_intervention: Whether human help was needed
        learnings: List of learnings from the task

    Returns:
        Updated agent data dict
    """
    ensure_directories()

    agent_file = LEARNINGS_DIR / f"{agent}.json"

    # Load existing data or create new
    if agent_file.exists():
        with open(agent_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {
            "agent": agent,
            "tasks": [],
            "learnings": [],
            "patterns": {},
            "created": datetime.now().isoformat()
        }

    # Add task record
    task_record = {
        "timestamp": datetime.now().isoformat(),
        "task_type": task_type,
        "success": success,
        "duration_minutes": duration_minutes,
        "blockers": blockers or [],
        "human_intervention": human_intervention,
        "learnings": learnings or []
    }
    data["tasks"].append(task_record)

    # Extract learnings
    if learnings:
        for learning in learnings:
            data["learnings"].append({
                "timestamp": datetime.now().isoformat(),
                "learning": learning,
                "source": task_type
            })

    # Detect patterns (same blocker 3+ times triggers flag)
    if blockers:
        for blocker in blockers:
            if blocker not in data["patterns"]:
                data["patterns"][blocker] = 0
            data["patterns"][blocker] += 1

    # Update last modified
    data["last_updated"] = datetime.now().isoformat()

    # Save
    with open(agent_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return data


def get_agent_health(agent: str) -> dict:
    """
    Calculate agent health metrics from logged data.

    Args:
        agent: Name of the agent

    Returns:
        Health metrics dict
    """
    agent_file = LEARNINGS_DIR / f"{agent}.json"

    if not agent_file.exists():
        return {"status": "no_data", "agent": agent}

    with open(agent_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tasks = data.get("tasks", [])
    if not tasks:
        return {"status": "no_tasks", "agent": agent}

    # Filter to recent tasks (last 30 days)
    thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
    recent_tasks = [
        t for t in tasks
        if datetime.fromisoformat(t["timestamp"]).timestamp() > thirty_days_ago
    ]

    if not recent_tasks:
        recent_tasks = tasks[-50:]  # Fall back to last 50 tasks

    # Calculate metrics
    total = len(recent_tasks)
    successes = sum(1 for t in recent_tasks if t["success"])
    human_interventions = sum(1 for t in recent_tasks if t.get("human_intervention", False))
    total_duration = sum(t.get("duration_minutes", 0) for t in recent_tasks)
    avg_duration = total_duration / total if total > 0 else 0

    # Detect training needs (patterns with 3+ occurrences)
    training_needs = [k for k, v in data.get("patterns", {}).items() if v >= 3]

    return {
        "agent": agent,
        "period": datetime.now().strftime("%Y-W%W"),
        "metrics": {
            "tasks_completed": total,
            "tasks_successful": successes,
            "success_rate": round(successes / total, 3) if total > 0 else 0,
            "human_intervention_rate": round(human_interventions / total, 3) if total > 0 else 0,
            "avg_duration_minutes": round(avg_duration, 1)
        },
        "learnings_count": len(data.get("learnings", [])),
        "training_needs": training_needs,
        "last_updated": data.get("last_updated", "unknown")
    }


def detect_skill_gaps() -> list:
    """
    Scan all agents for skill gaps based on performance data.

    Returns:
        List of detected gaps with recommendations
    """
    ensure_directories()
    gaps = []

    for agent_file in LEARNINGS_DIR.glob("*.json"):
        agent = agent_file.stem
        health = get_agent_health(agent)

        if health.get("status"):
            continue

        metrics = health.get("metrics", {})

        # Flag if success rate < 80%
        if metrics.get("success_rate", 1) < 0.8:
            gaps.append({
                "agent": agent,
                "issue": "low_success_rate",
                "value": metrics["success_rate"],
                "severity": "high" if metrics["success_rate"] < 0.6 else "medium",
                "recommendation": "Review SKILL.md competencies and update training"
            })

        # Flag if human intervention > 20%
        if metrics.get("human_intervention_rate", 0) > 0.2:
            gaps.append({
                "agent": agent,
                "issue": "high_human_intervention",
                "value": metrics["human_intervention_rate"],
                "severity": "medium",
                "recommendation": "Add autonomy guidance to SKILL.md"
            })

        # Flag training needs from patterns
        for need in health.get("training_needs", []):
            gaps.append({
                "agent": agent,
                "issue": "recurring_blocker",
                "pattern": need,
                "severity": "medium",
                "recommendation": f"Add methodology or workflow for: {need}"
            })

    return gaps


def generate_report() -> dict:
    """
    Generate a full system health report.

    Returns:
        Report dict with all agent health and gaps
    """
    ensure_directories()

    agents = []
    for agent_file in LEARNINGS_DIR.glob("*.json"):
        agents.append(get_agent_health(agent_file.stem))

    gaps = detect_skill_gaps()

    # Calculate system-wide metrics
    total_tasks = sum(a.get("metrics", {}).get("tasks_completed", 0) for a in agents if "metrics" in a)
    total_successful = sum(a.get("metrics", {}).get("tasks_successful", 0) for a in agents if "metrics" in a)

    return {
        "generated": datetime.now().isoformat(),
        "period": datetime.now().strftime("%Y-W%W"),
        "system_metrics": {
            "total_agents_tracked": len(agents),
            "total_tasks": total_tasks,
            "system_success_rate": round(total_successful / total_tasks, 3) if total_tasks > 0 else 0,
            "gaps_detected": len(gaps)
        },
        "agents": agents,
        "gaps": gaps
    }


def log_incident(
    incident_id: str,
    severity: str,
    agents_involved: list,
    description: str,
    root_cause: str,
    resolution: str,
    learnings: list
) -> dict:
    """
    Log an incident for post-mortem analysis.

    Args:
        incident_id: Unique identifier
        severity: SEV1, SEV2, SEV3
        agents_involved: List of agent names
        description: What happened
        root_cause: Why it happened
        resolution: How it was fixed
        learnings: What we learned

    Returns:
        Incident record dict
    """
    ensure_directories()

    incident = {
        "id": incident_id,
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "agents_involved": agents_involved,
        "description": description,
        "root_cause": root_cause,
        "resolution": resolution,
        "learnings": learnings,
        "status": "documented"
    }

    # Save incident
    incident_file = INCIDENTS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}-{incident_id}.json"
    with open(incident_file, 'w', encoding='utf-8') as f:
        json.dump(incident, f, indent=2)

    # Also log learnings to each involved agent
    for agent in agents_involved:
        log_task_outcome(
            agent=agent,
            task_type="incident_response",
            success=True,
            learnings=learnings
        )

    return incident


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("""
Feedback Engine - AgOS 2.0

Usage:
    python feedback_engine.py log <agent> <task_type> <success> [--duration=N] [--blocker=X] [--learning=Y]
    python feedback_engine.py health <agent>
    python feedback_engine.py gaps
    python feedback_engine.py report

Examples:
    python feedback_engine.py log jonny-ai feature true --duration=15
    python feedback_engine.py health sentinel
    python feedback_engine.py gaps
    python feedback_engine.py report
        """)
        sys.exit(1)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 5:
            print("Usage: python feedback_engine.py log <agent> <task_type> <success>")
            sys.exit(1)

        agent = sys.argv[2]
        task_type = sys.argv[3]
        success = sys.argv[4].lower() in ('true', '1', 'yes')

        # Parse optional args
        duration = 0
        blockers = []
        learnings = []
        human = False

        for arg in sys.argv[5:]:
            if arg.startswith('--duration='):
                duration = int(arg.split('=')[1])
            elif arg.startswith('--blocker='):
                blockers.append(arg.split('=')[1])
            elif arg.startswith('--learning='):
                learnings.append(arg.split('=')[1])
            elif arg == '--human':
                human = True

        result = log_task_outcome(
            agent=agent,
            task_type=task_type,
            success=success,
            duration_minutes=duration,
            blockers=blockers,
            learnings=learnings,
            human_intervention=human
        )
        print(f"Logged task for {agent}: {task_type} ({'success' if success else 'failure'})")

    elif command == "health":
        if len(sys.argv) < 3:
            print("Usage: python feedback_engine.py health <agent>")
            sys.exit(1)

        agent = sys.argv[2]
        health = get_agent_health(agent)
        print(json.dumps(health, indent=2))

    elif command == "gaps":
        gaps = detect_skill_gaps()
        print(json.dumps(gaps, indent=2))

    elif command == "report":
        report = generate_report()
        print(json.dumps(report, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
