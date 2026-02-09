"""
Memory Quality Gate — Jai.OS 4.0
Validates learnings before they enter the permanent memory system.
Prevents memory pollution through confidence scoring, novelty checks,
temporal decay, and verified/experimental separation.

Usage:
    python execution/memory_quality_gate.py validate --learning "Your learning text" --source "T029" --confidence 0.9
    python execution/memory_quality_gate.py decay                # Apply temporal decay to all memories
    python execution/memory_quality_gate.py report               # Show memory health report
    python execution/memory_quality_gate.py prune --threshold 0.3  # Remove low-weight memories
"""

import json
import sys
import math
import argparse
from pathlib import Path
from datetime import datetime, timezone
from difflib import SequenceMatcher

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).parent.parent
TASK_HISTORY = ROOT_DIR / ".agent" / "memory" / "task-history.json"
LEARNING_RUNS = ROOT_DIR / ".agent" / "memory" / "learning-runs.json"
AGENT_HEALTH = ROOT_DIR / ".agent" / "memory" / "agent-health.json"

# Quality thresholds
CONFIDENCE_THRESHOLD = 0.7       # Minimum confidence to enter permanent memory
NOVELTY_THRESHOLD = 0.5          # Below this similarity = novel enough to add
DECAY_RATE = 0.1                 # Exponential decay rate (per day)
PRUNE_THRESHOLD = 0.3            # Below this weight = candidate for pruning
MAX_LEARNINGS = 50               # Cap on total learnings in task-history


def load_json(path):
    """Load a JSON file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[WARN] Could not load {path}: {e}")
        return None


def save_json(path, data):
    """Save data to JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved {path}")


def similarity(a, b):
    """Calculate text similarity between two strings (0.0 to 1.0)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def validate_learning(learning_text, source, confidence, dry_run=False):
    """
    Validate a learning before adding it to permanent memory.
    Returns (approved, reason).
    """
    print(f"\n{'='*60}")
    print(f"  MEMORY QUALITY GATE — Validating Learning")
    print(f"{'='*60}")
    print(f"  Text: {learning_text[:80]}...")
    print(f"  Source: {source}")
    print(f"  Confidence: {confidence}")
    print()

    # Gate 1: Confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        reason = f"REJECTED: Confidence {confidence} < threshold {CONFIDENCE_THRESHOLD}. Route to experimental pool."
        print(f"  [GATE 1] ❌ {reason}")
        return False, reason
    print(f"  [GATE 1] ✅ Confidence {confidence} >= {CONFIDENCE_THRESHOLD}")

    # Gate 2: Novelty check (dedup against existing learnings)
    history = load_json(TASK_HISTORY)
    if history and "recent_learnings" in history:
        for existing in history["recent_learnings"]:
            sim = similarity(learning_text, existing.get("learning", ""))
            if sim > (1 - NOVELTY_THRESHOLD):
                reason = f"REJECTED: Too similar to existing learning (similarity={sim:.2f}). Existing: '{existing['learning'][:60]}...'"
                print(f"  [GATE 2] ❌ {reason}")
                return False, reason
    print(f"  [GATE 2] ✅ Novel (no duplicates found)")

    # Gate 3: Cap check
    if history and "recent_learnings" in history:
        if len(history["recent_learnings"]) >= MAX_LEARNINGS:
            reason = f"REJECTED: Memory at capacity ({MAX_LEARNINGS} learnings). Run 'prune' first."
            print(f"  [GATE 3] ❌ {reason}")
            return False, reason
    print(f"  [GATE 3] ✅ Under capacity")

    # Gate 4: Non-empty check
    if len(learning_text.strip()) < 10:
        reason = "REJECTED: Learning text too short (< 10 chars)."
        print(f"  [GATE 4] ❌ {reason}")
        return False, reason
    print(f"  [GATE 4] ✅ Content valid")

    # All gates passed
    print(f"\n  ✅ APPROVED — Learning passes all quality gates")

    if not dry_run and history:
        new_learning = {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "learning": learning_text,
            "source": source,
            "confidence": confidence,
            "weight": 1.0,
            "pool": "verified" if confidence >= 0.9 else "experimental"
        }
        history["recent_learnings"].append(new_learning)
        save_json(TASK_HISTORY, history)
        print(f"  📝 Added to {new_learning['pool']} pool in task-history.json")

    return True, "APPROVED"


def apply_temporal_decay():
    """Apply exponential decay to all learning weights based on age."""
    print(f"\n{'='*60}")
    print(f"  TEMPORAL DECAY — Reducing weight of older memories")
    print(f"{'='*60}")

    history = load_json(TASK_HISTORY)
    if not history or "recent_learnings" not in history:
        print("  [WARN] No learnings found to decay")
        return

    now = datetime.now(timezone.utc)
    decayed = 0

    for learning in history["recent_learnings"]:
        try:
            learning_date = datetime.strptime(learning["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            age_days = (now - learning_date).days
            current_weight = learning.get("weight", 1.0)
            new_weight = current_weight * math.exp(-DECAY_RATE * age_days)
            new_weight = max(new_weight, 0.01)  # Floor at 0.01

            if abs(new_weight - current_weight) > 0.001:
                learning["weight"] = round(new_weight, 4)
                decayed += 1
                print(f"  [{learning['date']}] {learning['learning'][:50]}... | {current_weight:.3f} → {new_weight:.3f}")
        except (ValueError, KeyError):
            continue

    save_json(TASK_HISTORY, history)
    print(f"\n  Decayed {decayed} learnings. Run 'prune' to remove low-weight entries.")


def prune_memories(threshold=None):
    """Remove learnings below the weight threshold."""
    threshold = threshold or PRUNE_THRESHOLD
    print(f"\n{'='*60}")
    print(f"  PRUNE — Removing learnings with weight < {threshold}")
    print(f"{'='*60}")

    history = load_json(TASK_HISTORY)
    if not history or "recent_learnings" not in history:
        print("  [WARN] No learnings found")
        return

    before = len(history["recent_learnings"])
    pruned = [l for l in history["recent_learnings"] if l.get("weight", 1.0) < threshold]
    history["recent_learnings"] = [l for l in history["recent_learnings"] if l.get("weight", 1.0) >= threshold]
    after = len(history["recent_learnings"])

    for p in pruned:
        print(f"  🗑️  [{p['date']}] {p['learning'][:60]}... (weight: {p.get('weight', 'N/A')})")

    save_json(TASK_HISTORY, history)
    print(f"\n  Pruned {before - after} learnings. {after} remaining.")


def memory_report():
    """Generate a memory health report."""
    print(f"\n{'='*60}")
    print(f"  MEMORY HEALTH REPORT — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    # Task History
    history = load_json(TASK_HISTORY)
    if history:
        tasks = history.get("tasks", [])
        learnings = history.get("recent_learnings", [])
        print(f"\n  📋 Task History:")
        print(f"     Total tasks: {len(tasks)}")
        print(f"     Success rate: {history.get('summary', {}).get('success_rate', 'N/A')}")
        print(f"     Learnings: {len(learnings)}")

        verified = [l for l in learnings if l.get("pool") == "verified"]
        experimental = [l for l in learnings if l.get("pool") == "experimental"]
        unclassified = [l for l in learnings if "pool" not in l]
        print(f"     Verified pool: {len(verified)}")
        print(f"     Experimental pool: {len(experimental)}")
        print(f"     Unclassified: {len(unclassified)}")

        if learnings:
            weights = [l.get("weight", 1.0) for l in learnings]
            print(f"     Avg weight: {sum(weights)/len(weights):.3f}")
            print(f"     Min weight: {min(weights):.3f}")
            print(f"     Max weight: {max(weights):.3f}")
    else:
        print(f"\n  ⚠️  Task history not found!")

    # Learning Runs
    runs = load_json(LEARNING_RUNS)
    if runs:
        print(f"\n  🏃 Learning Runs:")
        print(f"     Total runs: {len(runs)}")
        for run in runs:
            print(f"     [{run.get('id')}] {run.get('task', 'Unknown')[:50]} — {run.get('result', 'N/A')}")
    else:
        print(f"\n  ⚠️  Learning runs not found!")

    # Agent Health
    health = load_json(AGENT_HEALTH)
    if health:
        summary = health.get("summary", {})
        print(f"\n  🤖 Agent Health:")
        print(f"     Total agents: {summary.get('total_agents', 'N/A')}")
        print(f"     Active: {summary.get('active', 'N/A')}")
        print(f"     Standby: {summary.get('standby', 'N/A')}")
        print(f"     System success rate: {summary.get('system_success_rate', 'N/A')}")
        gaps = health.get("gaps_detected", [])
        if gaps:
            print(f"     Gaps detected: {len(gaps)}")
            for gap in gaps:
                print(f"       - [{gap.get('severity', 'N/A')}] {gap.get('description', 'N/A')[:60]}")
    else:
        print(f"\n  ⚠️  Agent health not found!")

    print(f"\n{'='*60}")
    print(f"  END REPORT")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Memory Quality Gate — Jai.OS 4.0")
    subparsers = parser.add_subparsers(dest="command")

    # validate
    val_parser = subparsers.add_parser("validate", help="Validate a learning before adding to memory")
    val_parser.add_argument("--learning", required=True, help="The learning text")
    val_parser.add_argument("--source", required=True, help="Source task ID (e.g., T029)")
    val_parser.add_argument("--confidence", type=float, required=True, help="Confidence score (0.0-1.0)")
    val_parser.add_argument("--dry-run", action="store_true", help="Validate without saving")

    # decay
    subparsers.add_parser("decay", help="Apply temporal decay to all memories")

    # prune
    prune_parser = subparsers.add_parser("prune", help="Remove low-weight memories")
    prune_parser.add_argument("--threshold", type=float, default=PRUNE_THRESHOLD, help=f"Weight threshold (default: {PRUNE_THRESHOLD})")

    # report
    subparsers.add_parser("report", help="Show memory health report")

    args = parser.parse_args()

    if args.command == "validate":
        validate_learning(args.learning, args.source, args.confidence, args.dry_run)
    elif args.command == "decay":
        apply_temporal_decay()
    elif args.command == "prune":
        prune_memories(args.threshold)
    elif args.command == "report":
        memory_report()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
