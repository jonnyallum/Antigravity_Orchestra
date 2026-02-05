
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# AgOS 3.0 Brain Sync Protocol Orchestrator
# Executes the full synchronization lifecycle

ROOT_DIR = Path(__file__).parent.parent

def run_step(name, command):
    print(f"\n>>> [STEP] {name}")
    print(f"Running: {command}")
    try:
        # Using shell=True for Windows compatibility with scripts
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=ROOT_DIR)
        if result.returncode == 0:
            print(f"[OK] {name} Success")
            if result.stdout:
                print(result.stdout.strip())
            return True
        else:
            print(f"[FAIL] {name} Failed (Exit {result.returncode})")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"[ERR] Error executing {name}: {e}")
        return False

def brain_sync_protocol():
    print(f"============================================================")
    print(f"   AgOS 3.0 BRAIN SYNC PROTOCOL - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"============================================================")

    steps = [
        ("VALIDATE AGENTS", "python execution/validate_agents.py"),
        ("REPORT SESSION", "python execution/session_logger.py report --days=1"),
        ("PUSH LEARNINGS", "python execution/brain_sync.py"),
        ("AUTO-COMMIT & PUSH", "python execution/auto_commit.py --push"),
        ("WEBSITE SYNC", "python execution/sync_to_website.py"),
        ("CHATROOM BROADCAST", 'python execution/brain_cli.py chat "SYSTEM SYNC COMPLETE: Orchestra synchronized, progress saved, and website updated. Ready for fresh tasks." --agent marcus'),
        ("LOCAL LOG SYNC", 'python -c "from pathlib import Path; from datetime import datetime; log = Path(\'.agent/boardroom/chatroom.md\'); content = f\'\\n### 🔄 SYSTEM SYNC COMPLETE\\n**Status:** SUCCESS\\n**Timestamp:** {datetime.now().strftime(\'%Y-%m-%d %H:%M\')}\\nAll systems aligned. Readiness: 100%.\\n---\\n\'; open(log, \'a\', encoding=\'utf-8\').write(content)"'),
        ("REDUNDANCY PURGE", "python execution/purge_redundant.py")
    ]

    results = []
    for name, cmd in steps:
        success = run_step(name, cmd)
        results.append((name, success))

    print(f"\n" + "="*60)
    print(f"   SYNC PROTOCOL SUMMARY")
    print(f"="*60)
    for name, success in results:
        status = "OK" if success else "FAIL"
        print(f" [{status}] : {name}")
    print(f"="*60)
    
    if all(r[1] for r in results):
        print("\nSYSTEM IS IN LINE. READY FOR FRESH MISSIONS.")
    else:
        print("\nSYNC PARTIALLY FAILED. CHECK LOGS.")

if __name__ == "__main__":
    brain_sync_protocol()
