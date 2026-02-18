"""
sync_learnings.py
Parses each agent's SKILL.md and syncs individual learnings to the
Supabase 'learnings' table in the Antigravity Shared Brain.

Schema: source_agent, learning, category, tags[], propagate_to[], verified
"""

import urllib.request
import urllib.error
import json
import os
import re

SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxrd3lkcXRmYmRqaHhhYXJlbGF6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDI5ODI4MiwiZXhwIjoyMDg1ODc0MjgyfQ.35gJkeetflYO5FYXrjELwikxqFvcScxFCQr5qDD-Z24"
BASE = "https://lkwydqtfbdjhxaarelaz.supabase.co/rest/v1"
SKILLS_DIR = r"C:\Users\jonny\Desktop\JonnyAI_JaiOS_4.0\.agent\skills"

HEADERS = {
    "apikey": SERVICE_KEY,
    "Authorization": "Bearer " + SERVICE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def api_post(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE}/learnings", data=data, headers=HEADERS, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:200]}"

def infer_category(text):
    t = text.lower()
    if any(w in t for w in ["deploy", "build", "server", "ssh", "ftp", "hostinger", "vercel", "next", "static"]):
        return "deployment"
    if any(w in t for w in ["supabase", "database", "sql", "schema", "table", "rls", "postgres"]):
        return "database"
    if any(w in t for w in ["seo", "meta", "sitemap", "robots", "schema.org", "google"]):
        return "seo"
    if any(w in t for w in ["design", "ui", "css", "tailwind", "figma", "color", "font", "layout"]):
        return "design"
    if any(w in t for w in ["security", "auth", "jwt", "oauth", "encrypt", "gdpr", "rls"]):
        return "security"
    if any(w in t for w in ["test", "qa", "verify", "check", "validate", "audit"]):
        return "quality"
    if any(w in t for w in ["api", "mcp", "webhook", "integration", "endpoint"]):
        return "integration"
    if any(w in t for w in ["bet", "odds", "racing", "football", "darts", "f1", "motogp"]):
        return "betting"
    if any(w in t for w in ["research", "analysis", "data", "report", "intelligence"]):
        return "research"
    if any(w in t for w in ["workflow", "process", "sop", "protocol", "automation"]):
        return "workflow"
    return "technical"

def infer_tags(text, handle):
    tags = [handle]
    t = text.lower()
    tag_map = {
        "nextjs": ["next.js", "next build", "trailingslash", "static export"],
        "deployment": ["deploy", "hostinger", "vercel", "ftp", "ssh", "upload"],
        "supabase": ["supabase", "postgres", "rls", "realtime"],
        "typescript": ["typescript", "tsx", "ts"],
        "tailwind": ["tailwind"],
        "seo": ["seo", "sitemap", "robots", "meta", "schema.org"],
        "security": ["security", "auth", "jwt", "encrypt", "gdpr"],
        "testing": ["test", "qa", "verify", "validate"],
        "mcp": ["mcp", "model context protocol"],
        "betting": ["bet", "odds", "racing", "football", "darts"],
        "performance": ["performance", "lighthouse", "core web vitals", "speed"],
        "git": ["git", "commit", "branch", "push"],
        "api": ["api", "endpoint", "rest", "webhook"],
        "design": ["figma", "ui", "ux", "design", "css"],
    }
    for tag, keywords in tag_map.items():
        if any(kw in t for kw in keywords):
            tags.append(tag)
    return list(set(tags))[:8]  # max 8 tags

def parse_skill_md(content, handle):
    """Extract individual learnings from a SKILL.md file."""
    learnings = []

    # Pattern 1: Numbered list items (1. Learning text)
    numbered = re.findall(r'^\s*\d+\.\s+\*\*(.+?)\*\*[:\s]*(.+?)(?=\n\s*\d+\.|\n\s*##|\Z)',
                          content, re.MULTILINE | re.DOTALL)
    for title, detail in numbered:
        text = f"{title.strip()}: {detail.strip()[:300]}"
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 20:
            learnings.append(text)

    # Pattern 2: Bold headers followed by content
    bold_items = re.findall(r'\*\*([^*\n]{10,80})\*\*[:\s]*([^\n*#]{20,300})', content)
    for title, detail in bold_items:
        text = f"{title.strip()}: {detail.strip()}"
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 30 and text not in [l for l in learnings]:
            learnings.append(text)

    # Pattern 3: Bullet points under "Learnings" or "Key Learnings" sections
    sections = re.split(r'\n#{1,3}\s+', content)
    for section in sections:
        if any(kw in section[:50].lower() for kw in ['learning', 'lesson', 'key insight', 'sop', 'rule', 'protocol']):
            bullets = re.findall(r'[-*]\s+(.{20,400}?)(?=\n[-*]|\n\n|\Z)', section, re.DOTALL)
            for b in bullets:
                text = re.sub(r'\s+', ' ', b).strip()
                if len(text) > 20:
                    learnings.append(text)

    # Deduplicate and limit
    seen = set()
    unique = []
    for l in learnings:
        key = l[:60].lower()
        if key not in seen and len(l) > 20:
            seen.add(key)
            unique.append(l[:500])  # max 500 chars per learning

    return unique[:30]  # max 30 learnings per agent

# ── Main sync ─────────────────────────────────────────────────────────────────
print("=" * 60)
print("ANTIGRAVITY SHARED BRAIN - LEARNINGS SYNC")
print("=" * 60)

skill_dirs = sorted([d for d in os.listdir(SKILLS_DIR)
                     if os.path.isdir(os.path.join(SKILLS_DIR, d)) and d != "methodology"])

total_ok = 0
total_fail = 0
total_skipped = 0

for handle in skill_dirs:
    path = os.path.join(SKILLS_DIR, handle, "SKILL.md")
    if not os.path.exists(path):
        total_skipped += 1
        continue

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    learnings = parse_skill_md(content, handle)

    if not learnings:
        print(f"  [SKIP] @{handle}: no parseable learnings")
        total_skipped += 1
        continue

    agent_ok = 0
    agent_fail = 0
    for learning_text in learnings:
        payload = {
            "source_agent": handle,
            "source_project": "jaios-4.0-skill-sync",
            "source_ai": "claude",
            "learning": learning_text,
            "category": infer_category(learning_text),
            "tags": infer_tags(learning_text, handle),
            "propagate_to": [],
            "verified": False,
            "applied_count": 0,
        }
        result, err = api_post(payload)
        if err:
            agent_fail += 1
        else:
            agent_ok += 1

    total_ok += agent_ok
    total_fail += agent_fail
    print(f"  [OK] @{handle}: {agent_ok} learnings synced" + (f", {agent_fail} failed" if agent_fail else ""))

print()
print("=" * 60)
print(f"LEARNINGS SYNC COMPLETE")
print(f"  Total synced:  {total_ok}")
print(f"  Total failed:  {total_fail}")
print(f"  Agents skipped (no SKILL.md): {total_skipped}")
print("=" * 60)
