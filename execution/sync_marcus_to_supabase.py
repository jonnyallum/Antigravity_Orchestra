"""
Sync Marcus (conductor) SKILL.md philosophy to Supabase agents table.
Reads credentials from JonnyAI_JaiOS_4.0/.env
"""
from pathlib import Path

WORKSPACE = Path(r"C:\Users\jonny\Desktop\AgOS 3.0 template")
ENV_PATH  = Path(r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0\.env")

# ── Load credentials ───────────────────────────────────────────────────────────
env = {}
for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()

SUPABASE_URL = env.get("NEXT_PUBLIC_SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = env.get("SUPABASE_SERVICE_ROLE_KEY", "")

print(f"URL   : {SUPABASE_URL[:45] if SUPABASE_URL else 'NOT FOUND'}")
print(f"Key   : {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "Key   : NOT FOUND")

if not SUPABASE_URL or not SUPABASE_KEY or "your-project" in SUPABASE_URL:
    raise SystemExit("[ERROR] No valid Supabase credentials found.")

# ── Read SKILL.md ──────────────────────────────────────────────────────────────
skill_path = WORKSPACE / ".agent" / "skills" / "conductor" / "SKILL.md"
skill_content = skill_path.read_text(encoding="utf-8")
print(f"SKILL : {len(skill_content.encode())/1024:.1f}KB read from {skill_path.name}")

# ── Connect to Supabase ────────────────────────────────────────────────────────
try:
    from supabase import create_client
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "supabase", "-q"], check=True)
    from supabase import create_client

sb = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── List available handles so we can confirm the right one ────────────────────
rows = sb.table("agents").select("handle,name,role").order("handle").execute()
print(f"\nAgents in DB: {len(rows.data)} rows")
conductors = [r for r in rows.data if "conductor" in (r.get("handle","") or "").lower()
              or "marcus" in (r.get("name","") or "").lower()
              or "maestro" in str(r).lower()]
print(f"Conductor candidates: {conductors}")

# ── Update ─────────────────────────────────────────────────────────────────────
if conductors:
    handle = conductors[0]["handle"]
    result = sb.table("agents").update({
        "philosophy": skill_content,
    }).eq("handle", handle).execute()
    print(f"\n[OK] Updated handle='{handle}' — {len(result.data)} row(s) affected")
else:
    # Try all possible handle variants
    for h in ["conductor", "marcus", "Conductor", "Marcus"]:
        result = sb.table("agents").update({
            "philosophy": skill_content,
        }).eq("handle", h).execute()
        if result.data:
            print(f"\n[OK] Updated handle='{h}' — {len(result.data)} row(s) affected")
            break
    else:
        print("\n[WARN] Could not match conductor/Marcus — printing all handles:")
        for r in rows.data:
            print(f"  {r['handle']!r:30} {r.get('name','')!r:30} {r.get('role','')!r}")

print("\nDONE")
