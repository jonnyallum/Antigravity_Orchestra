"""
Extract Agent Roster from SKILL.md Files
Generates a comprehensive agent roster table for documentation sync.
"""

import os
import re
from pathlib import Path

def extract_agent_metadata(skill_path):
    """Extract key metadata from a SKILL.md file."""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract from Identity table
        handle = re.search(r'\*\*Agent Handle\*\*\s*\|\s*@?(\w+)', content)
        human_name = re.search(r'\*\*Human Name\*\*\s*\|\s*([^\r\n|]+)', content)
        nickname = re.search(r'\*\*Nickname\*\*\s*\|\s*"?([^"\r\n|]+)"?', content)
        role = re.search(r'\*\*Role\*\*\s*\|\s*([^\r\n|]+)', content)
        
        return {
            'handle': handle.group(1).strip() if handle else None,
            'human_name': human_name.group(1).strip() if human_name else None,
            'nickname': nickname.group(1).strip() if nickname else None,
            'role': role.group(1).strip() if role else None
        }
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

def main():
    skills_dir = Path('.agent/skills')
    agents = []
    
    # Scan all agent skill folders
    for agent_dir in sorted(skills_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        
        # Skip special folders
        if agent_dir.name in ['methodology', 'learning-coordinator']:
            continue
        
        skill_file = agent_dir / 'SKILL.md'
        if not skill_file.exists():
            print(f"⚠️  Missing SKILL.md for {agent_dir.name}")
            continue
        
        metadata = extract_agent_metadata(skill_file)
        if metadata and all(metadata.values()):
            agents.append(metadata)
        else:
            print(f"⚠️  Incomplete metadata for {agent_dir.name}")
    
    print(f"\n✅ Extracted {len(agents)} agents\n")
    print("=" * 100)
    print("AGENT ROSTER TABLE (Markdown Format)")
    print("=" * 100)
    print("\n| Handle | Human Name | Nickname | Role |")
    print("|:-------|:-----------|:---------|:-----|")
    
    for agent in agents:
        print(f"| **@{agent['handle'].capitalize()}** | {agent['human_name']} | \"{agent['nickname']}\" | {agent['role']} |")
    
    print(f"\n\n✅ Total Agents: {len(agents)}")
    print("=" * 100)

if __name__ == "__main__":
    main()
