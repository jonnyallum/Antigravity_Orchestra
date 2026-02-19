# master_hydration.py
# Syncs newer content from AgOS 3.0 Template -> JonnyAI_JaiOS_4.0 Master
# This "Hydrates" the master repository with client work and new ecosystem data.

import os
import shutil
import subprocess
from datetime import datetime

TEMPLATE = r"C:\Users\jonny\Desktop\AgOS 3.0 template"
MASTER   = r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0"

# Files/Folders to exclude from sync
EXCLUDES = [
    ".git",
    "node_modules",
    ".next",
    "out",
    ".tmp",
    ".gemini",
    "__pycache__",
    ".vercel",
    "build_output.log"
]

def hydrate():
    print("=" * 60)
    print("MASTER HYDRATION PROTOCOL: Template -> Jai.OS 4.0 Master")
    print(f"Source: {TEMPLATE}")
    print(f"Target: {MASTER}")
    print("=" * 60)

    if not os.path.exists(MASTER):
        print(f"[FAIL] Master directory not found at {MASTER}")
        return

    # Using Robocopy for high-performance sync on Windows
    # /E - Subdirectories (including empty)
    # /Z - Restartable mode
    # /XO - Exclude Older (only copy if source is newer)
    # /XF - Exclude Files
    # /XD - Exclude Directories
    
    cmd = [
        "robocopy",
        TEMPLATE,
        MASTER,
        "/E",
        "/XO",
        "/NS", "/NC", "/NFL", "/NDL", "/NP", # Quiet mode items
        "/XD"
    ] + EXCLUDES + [
        "/XF"
    ] + EXCLUDES

    print("Running Robocopy sync...")
    # Robocopy exit codes are bitmasks (1-3 are successful copies/tweaks)
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode < 8:
        print("[OK] Master hydrated successfully.")
    else:
        print(f"[ERROR] Robocopy failed with code {result.returncode}")
        print(result.stdout)
        print(result.stderr)

    # ── Verify Specific Mission-Critical Folders ──────────────────────────────
    critical_paths = [
        "Clients/jsc-contractors",
        "Ecosystems/Trading-Floor",
        "execution/ralph_loop.py"
    ]
    
    print("\nVerifying hydration status:")
    for path in critical_paths:
        target = os.path.join(MASTER, path)
        if os.path.exists(target):
            print(f"  [FOUND] {path}")
        else:
            print(f"  [MISSING] {path}")

    print("\n" + "=" * 60)
    print(f"PROTOCOL COMPLETE | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == "__main__":
    hydrate()
