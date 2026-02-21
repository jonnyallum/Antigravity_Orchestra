"""
Sync Marcus (conductor) SKILL.md to Supabase agents table + push to GitHub.
"""
import os, subprocess
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0")

# ── Load .env ──────────────────────────────────────────────────────────────────
env = {}
env_path = WORKSPACE / ".env"
if env_path.exists():
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()

SUPABASE_URL = env.get("NEXT_PUBLIC_SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = env.get("SUPABASE_SERVICE_ROLE_KEY", "")

if not SUPABASE_URL or not SUPABASE_KEY or "your-project" in SUPABASE_URL:
    print("[WARN] No valid Supabase credentials in .env — skipping DB sync")
    print(f"  URL found: {bool(SUPABASE_URL)}, Key found: {bool(SUPABASE_KEY)}")
else:
    try:
        from supabase import create_client
    except ImportError:
        print("[INFO] Installing supabase-py...")
        subprocess.run(["pip", "install", "supabase", "-q"])
        from supabase import create_client

    skill_path = WORKSPACE / ".agent" / "skills" / "marcus" / "SKILL.md"
    skill_content = skill_path.read_text(encoding="utf-8")
    print(f"[OK] Read SKILL.md — {len(skill_content.encode())/1024:.1f}KB")

    sb = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Try handle 'marcus' first, then fall back to name match
    result = sb.table("agents").update({
        "philosophy": skill_content,
        "updated_at": "now()"
    }).eq("handle", "marcus").execute()

    if result.data:
        print(f"[OK] Supabase updated — handle=conductor ({len(result.data)} row)")
    else:
        # Fallback: try matching by name
        result2 = sb.table("agents").update({
            "philosophy": skill_content,
            "updated_at": "now()"
        }).ilike("name", "%Marcus%").execute()

        if result2.data:
            print(f"[OK] Supabase updated — name~Marcus ({len(result2.data)} row)")
        else:
            # Show available handles so we can diagnose
            rows = sb.table("agents").select("handle,name").limit(50).execute()
            handles = [(r["handle"], r.get("name","")) for r in rows.data]
            print("[WARN] No rows matched. Available agent handles:")
            for h, n in handles[:20]:
                print(f"  {h} — {n}")

# ── Git commit + push ──────────────────────────────────────────────────────────
os.chdir(WORKSPACE)
subprocess.run(["git", "add", ".agent/skills/conductor/SKILL.md"])
r = subprocess.run(
    ["git", "commit", "-m",
     "[Marcus/conductor] Full Jai.OS 4.0 SKILL.md — SOPs, quality gates, self-annealing, safety | 2026-02-19"],
    capture_output=True, text=True
)
if r.returncode == 0:
    print(f"[OK] Committed: {r.stdout.strip().splitlines()[0]}")
else:
    print(f"[INFO] {r.stdout.strip() or r.stderr.strip()}")

r2 = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
if r2.returncode == 0:
    print("[OK] Pushed to GitHub main")
else:
    subprocess.run(["git", "pull", "--rebase", "origin", "main"])
    r3 = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
    print("[OK] Pushed after rebase" if r3.returncode == 0 else f"[FAIL] {r3.stderr.strip()[:100]}")

print("\nDONE")
