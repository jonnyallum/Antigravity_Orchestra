"""
upgrade_to_jaios4.py — Bulk upgrade all Jai.OS 4.0/3.0 references to Jai.OS 4.0
Built by @Cline for the Antigravity Orchestra.

SAFE: Only touches files in the master workspace (not Client submodules).
Creates a backup log of all changes made.

Usage:
    python execution/upgrade_to_jaios4.py --dry-run    # Preview changes
    python execution/upgrade_to_jaios4.py               # Apply changes
"""

import os
import sys
import re
import io
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).parent.parent
DRY_RUN = "--dry-run" in sys.argv

# Files/dirs to SKIP (client submodules have their own repos)
SKIP_DIRS = {
    "Clients/CD Waste",
    "Clients/DJ Waste", 
    "Clients/Insydetradar",
    "Clients/Joes #app",
    "Clients/La-Aesthetician.co.uk",
    "Clients/Poundtrades.app-antigravity",
    "Clients/Village-bakery",
    "Clients/DELETEME_LATER",
    "Clients/kwizz",
    "Clients/jonnyai.website",
    "Clients/AI-Clash",
    ".git",
    "node_modules",
    ".tmp",
}

# Replacement rules (order matters — most specific first)
REPLACEMENTS = [
    # Full branded names
    ("Jai.OS 4.0", "Jai.OS 4.0"),  # Already correct — skip
    ("Jai.OS 4.0", "Jai.OS 4.0"),
    ("Jai.OS 4.0", "Jai.OS 4.0"),
    ("Jai.OS 4.0 — The Hive Mind", "Jai.OS 4.0 — The Hive Mind"),
    
    # Headers and titles
    ("The Architecture (Jai.OS 4.0)", "The Architecture (Jai.OS 4.0)"),
    ("The Hive Mind Architecture (Jai.OS 4.0)", "The Hive Mind Architecture (Jai.OS 4.0)"),
    ("The Jai.OS 4.0", "The Jai.OS 4.0 Architecture"),
    ("The Jai.OS 4.0", "The Jai.OS 4.0 Architecture"),
    ("The Jai.OS 4.0 Philosophy", "The Jai.OS 4.0 Philosophy"),
    
    # Version stamps
    ("Jai.OS 4.0 Collaboration Protocol", "Jai.OS 4.0 Collaboration Protocol"),
    ("Jai.OS 4.0 Agent Orchestra", "Jai.OS 4.0 Agent Orchestra"),
    ("Jai.OS 4.0 Hive Mind", "Jai.OS 4.0 Hive Mind"),
    ("Jai.OS 4.0 Standard", "Jai.OS 4.0 Standard"),
    ("Jai.OS 4.0 Compliant", "Jai.OS 4.0 Compliant"),
    ("Jai.OS 4.0 Core", "Jai.OS 4.0 Core"),
    ("Jai.OS 4.0 Core", "Jai.OS 4.0 Core"),
    ("Jai.OS 4.0 Compliant", "Jai.OS 4.0 Compliant"),
    ("Jai.OS 4.0 Module Licensing", "Jai.OS 4.0 Module Licensing"),
    ("Jai.OS 4.0 Execution Engine", "Jai.OS 4.0 Execution Engine"),
    ("Jai.OS 4.0 Ecosystem Roadmap", "Jai.OS 4.0 Ecosystem Roadmap"),
    ("Jai.OS 4.0 Comprehensive Workspace Audit", "Jai.OS 4.0 Comprehensive Workspace Audit"),
    ("Jai.OS 4.0 workspace", "Jai.OS 4.0 workspace"),
    ("Jai.OS 4.0 implementation", "Jai.OS 4.0 implementation"),
    ("Jai.OS 4.0 framework", "Jai.OS 4.0 framework"),
    ("Jai.OS 4.0 orchestration layer", "Jai.OS 4.0 orchestration layer"),
    
    # Footers and timestamps
    ("Last updated: Jai.OS 4.0 — The Hive Mind", "Last updated: Jai.OS 4.0 — The Hive Mind"),
    ("Last updated: Jai.OS 4.0 — Universal Sync Active", "Last updated: Jai.OS 4.0 — Universal Sync Active"),
    ("Last Updated: Jai.OS 4.0", "Last Updated: Jai.OS 4.0"),
    
    # Subtitles
    ("Jai.OS 4.0 — The Hive Mind", "Jai.OS 4.0 — The Hive Mind"),
    ("Jai.OS 4.0 — The Hive Mind", "Jai.OS 4.0 — The Hive Mind"),
    
    # Generic catches (last — broadest)
    ("Powered by Antigravity Jai.OS 4.0", "Powered by Antigravity Jai.OS 4.0"),
    ("powered by Jai.OS 4.0", "powered by Jai.OS 4.0"),
    ("Jai.OS 4.0 //", "Jai.OS 4.0 //"),
    ("Jai.OS 4.0", "Jai.OS 4.0"),
    ("Jai.OS 4.0", "Jai.OS 4.0"),
]

# Also update the agent_summoner.py header
SUMMONER_REPLACEMENTS = [
    ("Jai.OS 4.0", "Jai.OS 4.0"),
]


def should_skip(filepath: Path) -> bool:
    """Check if file should be skipped."""
    rel = filepath.relative_to(ROOT).as_posix()
    for skip in SKIP_DIRS:
        if rel.startswith(skip):
            return True
    return False


def process_file(filepath: Path, changes_log: list) -> int:
    """Process a single file. Returns number of replacements made."""
    if should_skip(filepath):
        return 0
    
    # Only process text files
    if filepath.suffix not in ('.md', '.py', '.txt', '.html', '.json', '.yml', '.yaml', '.ts', '.tsx', '.js', '.css'):
        return 0
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        return 0
    
    original = content
    total_replacements = 0
    
    for old, new in REPLACEMENTS:
        if old == new:
            continue
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            total_replacements += count
            rel_path = filepath.relative_to(ROOT).as_posix()
            changes_log.append(f"  {rel_path}: '{old}' → '{new}' ({count}x)")
    
    if total_replacements > 0 and not DRY_RUN:
        filepath.write_text(content, encoding='utf-8')
    
    return total_replacements


def main():
    print("=" * 60)
    print(f"🔄 UPGRADE TO Jai.OS 4.0 {'(DRY RUN)' if DRY_RUN else '(LIVE)'}")
    print("=" * 60)
    
    changes_log = []
    total_files = 0
    total_replacements = 0
    
    # Walk all files
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip hidden dirs and node_modules
        dirnames[:] = [d for d in dirnames if not d.startswith('.') or d == '.agent']
        dirnames[:] = [d for d in dirnames if d != 'node_modules']
        
        for filename in filenames:
            filepath = Path(dirpath) / filename
            count = process_file(filepath, changes_log)
            if count > 0:
                total_files += 1
                total_replacements += count
    
    print(f"\n📊 Results:")
    print(f"  Files modified: {total_files}")
    print(f"  Total replacements: {total_replacements}")
    
    if changes_log:
        print(f"\n📝 Changes:")
        for entry in changes_log:
            print(entry)
    
    if DRY_RUN:
        print(f"\n⚠️  DRY RUN — no files were modified. Run without --dry-run to apply.")
    else:
        print(f"\n✅ All references upgraded to Jai.OS 4.0")
        
        # Save change log
        log_path = ROOT / ".tmp" / "jaios4_upgrade_log.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Jai.OS 4.0 Upgrade Log\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n")
            f.write(f"**Files Modified:** {total_files}\n")
            f.write(f"**Total Replacements:** {total_replacements}\n\n")
            f.write("## Changes\n")
            for entry in changes_log:
                f.write(f"{entry}\n")
        print(f"  Log saved to: .tmp/jaios4_upgrade_log.md")


if __name__ == "__main__":
    main()
