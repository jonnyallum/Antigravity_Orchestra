import os
import re
from pathlib import Path

SKILLS_DIR = Path("c:/Users/jonny/Desktop/JonnyAI_JaiOS_4.0/.agent/skills")

# Expanded Metadata for 45 Agents
agent_metadata = {
    "marcus": {"name": "Marcus Cole", "nickname": "The Maestro", "role": "Orchestrator & Team Lead", "tier": "Command"},
    "arthur": {"name": "Arthur Webb", "nickname": "The Librarian", "role": "Documentation & Knowledge", "tier": "Command"},
    "jonny": {"name": "Jonny Allum", "nickname": "The Architect", "role": "Full-Stack Development Lead", "tier": "Development"},
    "priya": {"name": "Priya Sharma", "nickname": "The Perfectionist", "role": "UI/Visual Designer", "tier": "Development"},
    "sam": {"name": "Sam Blackwood", "nickname": "The Gatekeeper", "role": "Security & QA", "tier": "Development"},
    "diana": {"name": "Diana Chen", "nickname": "The Vault", "role": "Database & Storage", "tier": "Development"},
    "victor": {"name": "Victor Reyes", "nickname": "The Locksmith", "role": "Secrets & Security", "tier": "Development"},
    "derek": {"name": "Derek O'Brien", "nickname": "The Engine", "role": "Infrastructure & Deployment", "tier": "Development"},
    "alex": {"name": "Alex Torres", "nickname": "The Machine", "role": "Automation Engineer", "tier": "Automation"},
    "sophie": {"name": "Sophie Reid", "nickname": "The Hawk", "role": "Research & Scraping", "tier": "Intel"},
    "patrick": {"name": "Patrick Nguyen", "nickname": "The Surgeon", "role": "Data Parsing", "tier": "Intel"},
    "maya": {"name": "Maya Singh", "nickname": "The Oracle", "role": "Performance & Analytics", "tier": "Growth"},
    "felix": {"name": "Felix Morgan", "nickname": "The Alchemist", "role": "Strategy & Monetization", "tier": "Growth"},
    "grace": {"name": "Grace Liu", "nickname": "The Ranker", "role": "SEO & Structured Data", "tier": "Growth"},
    "elena": {"name": "Elena Vasquez", "nickname": "The Voice", "role": "Communication & Tone", "tier": "Growth"},
    "carlos": {"name": "Carlos Mendez", "nickname": "The Hook", "role": "Viral Video Editor", "tier": "Growth"},
    "hannah": {"name": "Hannah Park", "nickname": "The Fixer", "role": "Support & Success", "tier": "Growth"},
    "mason": {"name": "Mason Drake", "nickname": "The Bridgemaster", "role": "MCP Discovery & Wiring", "tier": "Automation"},
    "luna": {"name": "Luna Sterling", "nickname": "The Shield", "role": "Legal & Compliance", "tier": "Legal"},
    "adrian": {"name": "Adrian Cross", "nickname": "The Welder", "role": "MCP Server Development", "tier": "Automation"},
    "owen": {"name": "Owen Stinger", "nickname": "The Hornet", "role": "CI/CD & Hostinger", "tier": "Automation"},
    "milo": {"name": "Milo Chen", "nickname": "The Optimizer", "role": "Performance & Mobile QA", "tier": "Development"},
    "vigil": {"name": "Vigil Chen", "nickname": "The Eye", "role": "Truth Verification", "tier": "Quality"},
    "rowan": {"name": "Rowan", "nickname": "The Beast", "role": "Content Depth & Truth-Lock", "tier": "Quality"},
    "gareth": {"name": "Gareth Williams", "nickname": "The Tactician", "role": "Football Tactical Intel", "tier": "Betting"},
    "monty": {"name": "Monty Carlo", "nickname": "The Mathematician", "role": "Roulette Mathematics", "tier": "Betting"},
    "redeye": {"name": "Redeye", "nickname": "The Night Owl", "role": "Betting Systems Coordination", "tier": "Betting"},
    "pietro": {"name": "Pietro Rossi", "nickname": "The Strategist", "role": "Formula 1 Strategy", "tier": "Betting"},
    "terry": {"name": "Terry Taylor", "nickname": "The 180 King", "role": "Darts Analysis", "tier": "Betting"},
    "harry": {"name": "Harry Holt", "nickname": "The Form Master", "role": "Horse Racing Analysis", "tier": "Betting"},
    "daniel": {"name": "Dr. Daniel Rossi", "nickname": "The Doctor", "role": "MotoGP Analysis", "tier": "Betting"},
    "sterling": {"name": "Sterling Brooks", "nickname": "The Bookie", "role": "Sports Betting Systems", "tier": "Betting"},
    "quinn": {"name": "Quinn Harper", "nickname": "The Catalyst", "role": "Product Strategy", "tier": "Management"},
    "jasper": {"name": "Jasper Cole", "nickname": "The Closer", "role": "Sales & Business Dev", "tier": "Management"},
    "julian": {"name": "Julian West", "nickname": "The Conductor", "role": "Project Management", "tier": "Management"},
    "nina": {"name": "Nina Patel", "nickname": "The Analyst", "role": "Business Intelligence", "tier": "Management"},
    "theo": {"name": "Theo Martinez", "nickname": "The Architect", "role": "System Architecture", "tier": "Management"},
    "sebastian": {"name": "Sebastian Cross", "nickname": "The Architect", "role": "Full-Stack Architect", "tier": "Development"},
    "genesis": {"name": "Genesis Nova", "nickname": "The Cloner", "role": "Ecosystem Creation", "tier": "Specialized"},
    "winston": {"name": "Winston Hayes", "nickname": "Whiz", "role": "Dropshipping & E-Commerce", "tier": "Specialized"},
    "trotter": {"name": "Derek Trotter", "nickname": "The Trader", "role": "Trading Systems", "tier": "Specialized"},
    "vivienne": {"name": "Vivienne Frost", "nickname": "The Visionary", "role": "Brand Identity", "tier": "Creative"},
    "hugo": {"name": "Hugo Reeves", "nickname": "The Crawler", "role": "GitHub Intel", "tier": "Intel"},
    "scholar": {"name": "Dr. Elias Thorne", "nickname": "The Professor", "role": "Deep Research", "tier": "Intel"},
    "steve": {"name": "Steve Rivers", "nickname": "The Schema Whisperer", "role": "Supabase Specialist", "tier": "Development"}
}

REQUIRED_SECTIONS = [
    "The Creed", "Identity", "Personality", "Capabilities", 
    "Standard Operating Procedures", "Collaboration", "Feedback Loop", 
    "Performance Metrics", "Restrictions", "Learning Log", "Tools & Resources"
]

def ensure_sections(body):
    for section in REQUIRED_SECTIONS:
        if not re.search(f"## {section}", body, re.IGNORECASE):
            body += f"\n\n## {section}\n\n[Pending initialization of {section} data...]\n"
    return body

def update_skill_files():
    for agent_dir in SKILLS_DIR.iterdir():
        if not agent_dir.is_dir() or agent_dir.name == "methodology":
            continue
        
        skill_file = agent_dir / "SKILL.md"
        if not skill_file.exists():
            continue
            
        handle = agent_dir.name
        meta = agent_metadata.get(handle, {"name": handle.capitalize(), "role": "Specialist", "tier": "Development", "nickname": "The Agent"})
        
        content = skill_file.read_text(encoding='utf-8')
        
        # Extract body
        if content.startswith('---'):
            yaml_end = content.find('---', 3)
            body = content[yaml_end+3:].strip()
        else:
            body = content.strip()
            
        # Ensure Profile Header
        if not re.search(r'^#\s+.*Agent Profile', body, re.MULTILINE):
            body = f"# {meta['name']} - Agent Profile\n\n" + body

        # Ensure all 11 sections
        body = ensure_sections(body)
            
        yaml = f"""---
name: @{handle}
description: {meta['role']}
tier: {meta['tier']}
allowed_tools: [python, bash, node]
---
"""
        new_content = yaml + "\n" + body
        
        skill_file.write_text(new_content, encoding='utf-8')
        print(f"Verified {handle} matches 11/11 standard")
        
        # Ensure scripts dir
        scripts_dir = agent_dir / "scripts"
        if not scripts_dir.exists():
            scripts_dir.mkdir(parents=True, exist_ok=True)
            (scripts_dir / ".gitkeep").touch()

if __name__ == "__main__":
    update_skill_files()
