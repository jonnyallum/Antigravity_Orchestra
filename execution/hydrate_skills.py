import re
import json
from pathlib import Path

ROOT_DIR = Path("c:/Users/jonny/Desktop/JonnyAI_JaiOS_4.0")
SKILLS_DIR = ROOT_DIR / ".agent" / "skills"
MEMORY_DIR = ROOT_DIR / ".agent" / "memory"

# Hardened mappings for mission-readiness
MISSION_DATA = {
    "vigil": {
        "verified_learnings": [
            "Detected stale HTML cache on Hostinger during 2026-02-11 deployment. Use ?cb=timestamp for verification.",
            "Placeholder detection protocol active. Fails build if 'Lorem Ipsum' or 'Coming Soon' found in public_html."
        ],
        "tool_links": "[verify_readiness.py](file:///c:/Users/jonny/Desktop/JonnyAI_JaiOS_4.0/execution/verify_readiness.py)"
    },
    "owen": {
        "verified_learnings": [
            "Hostinger FTP/SSH path mismatch resolved. Always use absolute paths for rsync.",
            "Zero-downtime deployment achieved via atomic symlink swap."
        ],
        "tool_links": "[deploy_v4.py](file:///c:/Users/jonny/Desktop/JonnyAI_JaiOS_4.0/execution/deploy_v4.py)"
    },
    "steve": {
        "verified_learnings": [
            "Supabase RLS policy 'authenticated' is too broad for public forms. Use specific service_role for imports.",
            "Brain sync latency reduced by batching psycopg2 inserts."
        ],
        "tool_links": "[brain_sync.py](file:///c:/Users/jonny/Desktop/JonnyAI_JaiOS_4.0/execution/brain_sync.py)"
    }
}

def hydrate_agent_skill(handle):
    skill_file = SKILLS_DIR / handle / "SKILL.md"
    if not skill_file.exists():
        return
    
    content = skill_file.read_text(encoding='utf-8')
    data = MISSION_DATA.get(handle, {})
    
    # 1. Replace placeholders in Learning Log
    if "verified_learnings" in data:
        log_entries = "\n".join([f"| {datetime.now().strftime('%Y-%m-%d')} | Shared Brain | {l} |" for l in data["verified_learnings"]])
        content = re.sub(r'\| \d{4}-\d{2}-\d{2} \| Initial \| \[Pending mission initialization...\] \|', log_entries, content)
    
    # 2. Update Tools & Resources
    if "tool_links" in data:
        content = re.sub(r'\[Pending tool initialization...\]', data["tool_links"], content)
    
    skill_file.write_text(content, encoding='utf-8')
    print(f"[+] Hydrated @{handle} with mission-ready data.")

if __name__ == "__main__":
    from datetime import datetime
    for agent in MISSION_DATA.keys():
        hydrate_agent_skill(agent)
