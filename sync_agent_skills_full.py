"""
sync_agent_skills_full.py
PATCHes each agent row in Supabase with the full SKILL.md content
stored in the 'philosophy' column (text field, currently null).
"""

import urllib.request
import urllib.error
import json
import os

SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxrd3lkcXRmYmRqaHhhYXJlbGF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDI5ODI4MiwiZXhwIjoyMDg1ODc0MjgyfQ.35gJkeetflYO5FYXrjELwikxqFvcScxFCQr5qDD-Z24"
BASE = "https://lkwydqtfbdjhxaarelaz.supabase.co/rest/v1"
SKILLS_DIR = r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0\.agent\skills"

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": "Bearer " + SERVICE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def patch_agent(handle, skill_content, learning_count):
    payload = {
        "philosophy": skill_content,
        "learning_count": learning_count,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}/agents?id=eq.{handle}",
        data=data,
        headers=HEADERS,
        method="PATCH"
    )
    try:
        resp = urllib.request.urlopen(req)
        return True, None
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode()[:200]}"

def count_learnings_for(handle, all_learnings):
    return sum(1 for l in all_learnings if l.get("source_agent") == handle)

# Get existing learning counts from DB
def get_all_learnings():
    req = urllib.request.Request(
        f"{BASE}/learnings?select=source_agent&limit=1000",
        headers=HEADERS
    )
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode())
    except:
        return []

print("=" * 60)
print("ANTIGRAVITY SHARED BRAIN - FULL SKILL SYNC")
print("Storing complete SKILL.md content in agents.philosophy")
print("=" * 60)

all_learnings = get_all_learnings()
print(f"Found {len(all_learnings)} learnings in DB to count")

skill_dirs = sorted([d for d in os.listdir(SKILLS_DIR)
                     if os.path.isdir(os.path.join(SKILLS_DIR, d)) and d != "methodology"])

ok = 0
fail = 0
no_skill = 0

for handle in skill_dirs:
    path = os.path.join(SKILLS_DIR, handle, "SKILL.md")

    if not os.path.exists(path):
        print(f"  [SKIP] @{handle}: no SKILL.md")
        no_skill += 1
        continue

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    lcount = count_learnings_for(handle, all_learnings)
    success, err = patch_agent(handle, content, lcount)

    if err:
        print(f"  [FAIL] @{handle}: {err[:100]}")
        fail += 1
    else:
        size_kb = len(content.encode("utf-8")) / 1024
        print(f"  [OK] @{handle}: {size_kb:.1f}KB skill stored, {lcount} learnings counted")
        ok += 1

print()
print("=" * 60)
print(f"FULL SKILL SYNC COMPLETE")
print(f"  Updated:  {ok} agents")
print(f"  Failed:   {fail} agents")
print(f"  Skipped:  {no_skill} (no SKILL.md)")
print("=" * 60)
print()
print("Full SKILL.md content is now in agents.philosophy column.")
