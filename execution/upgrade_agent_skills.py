
import os
import re
import yaml
from pathlib import Path

# Config
ROOT_DIR = Path(__file__).parent.parent
SKILLS_DIR = ROOT_DIR / ".agent" / "skills"
TEMPLATE_PATH = SKILLS_DIR / "SKILL_TEMPLATE.md"

# Agent metadata map from brain_sync.py
AGENT_META = {
    "marcus": ("Marcus Cole", "The Maestro", "Orchestrator & Team Lead", "Command"),
    "arthur": ("Arthur Webb", "The Librarian", "Documentation & Knowledge", "Command"),
    "jonny": ("Jonny Allum", "The Architect", "Full-Stack Development Lead", "Development"),
    "priya": ("Priya Sharma", "The Perfectionist", "UI/Visual Designer", "Development"),
    "sam": ("Sam Blackwood", "The Gatekeeper", "Security & QA", "Development"),
    "diana": ("Diana Chen", "The Vault", "Database & Storage", "Development"),
    "victor": ("Victor Reyes", "The Locksmith", "Secrets & Security", "Development"),
    "derek": ("Derek O'Brien", "The Engine", "Infrastructure & Deployment", "Development"),
    "alex": ("Alex Torres", "The Machine", "Automation Engineer", "Automation"),
    "sophie": ("Sophie Reid", "The Hawk", "Research & Scraping", "Intel"),
    "patrick": ("Patrick Nguyen", "The Surgeon", "Data Parsing", "Intel"),
    "maya": ("Maya Singh", "The Oracle", "Performance & Analytics", "Growth"),
    "felix": ("Felix Morgan", "The Alchemist", "Strategy & Monetization", "Growth"),
    "grace": ("Grace Liu", "The Ranker", "SEO & Structured Data", "Growth"),
    "elena": ("Elena Vasquez", "The Voice", "Communication & Tone", "Growth"),
    "carlos": ("Carlos Mendez", "The Hook", "Viral Video Editor", "Growth"),
    "hannah": ("Hannah Park", "The Fixer", "Support & Success", "Growth"),
    "mason": ("Mason Drake", "The Bridgemaster", "MCP Discovery & Wiring", "Automation"),
    "luna": ("Luna Sterling", "The Shield", "Legal & Compliance", "Legal"),
    "adrian": ("Adrian Cross", "The Welder", "MCP Server Development", "Automation"),
    "owen": ("Owen Stinger", "The Hornet", "CI/CD & Hostinger", "Automation"),
    "milo": ("Milo Chen", "The Optimizer", "Performance & Mobile QA", "Development"),
    "vigil": ("Vigil Chen", "The Eye", "Truth Verification", "Quality"),
    "rowan": ("Rowan", "The Beast", "Content Depth & Truth-Lock", "Quality"),
    "gareth": ("Gareth Williams", "The Tactician", "Football Tactical Intel", "Betting"),
    "monty": ("Monty Carlo", "The Mathematician", "Roulette Mathematics", "Betting"),
    "redeye": ("Redeye", "The Night Owl", "Betting Systems Coordination", "Betting"),
    "pietro": ("Pietro Rossi", "The Strategist", "Formula 1 Strategy", "Betting"),
    "terry": ("Terry Taylor", "The 180 King", "Darts Analysis", "Betting"),
    "harry": ("Harry Holt", "The Form Master", "Horse Racing Analysis", "Betting"),
    "daniel": ("Dr. Daniel Rossi", "The Doctor", "MotoGP Analysis", "Betting"),
    "sterling": ("Sterling Brooks", "The Bookie", "Sports Betting Systems", "Betting"),
    "quinn": ("Quinn Harper", "The Catalyst", "Product Strategy", "Management"),
    "jasper": ("Jasper Cole", "The Closer", "Sales & Business Dev", "Management"),
    "julian": ("Julian West", "The Conductor", "Project Management", "Management"),
    "nina": ("Nina Patel", "The Analyst", "Business Intelligence", "Management"),
    "theo": ("Theo Martinez", "The Architect", "System Architecture", "Management"),
    "sebastian": ("Sebastian Cross", "The Architect", "Full-Stack Architect", "Development"),
    "genesis": ("Genesis Nova", "The Cloner", "Ecosystem Creation", "Specialized"),
    "winston": ("Winston Hayes", "Whiz", "Dropshipping & E-Commerce", "Specialized"),
    "trotter": ("Derek Trotter", "The Trader", "Trading Systems", "Specialized"),
    "vivienne": ("Vivienne Frost", "The Visionary", "Brand Identity", "Creative"),
    "hugo": ("Hugo Reeves", "The Crawler", "GitHub Intel", "Intel"),
    "scholar": ("Dr. Elias Thorne", "The Professor", "Deep Research", "Intel"),
    "steve": ("Steve Rivers", "The Schema Whisperer", "Supabase Specialist", "Development")
}

DEFAULT_QUOTES = {
    "marcus": "The speed of the leader is the speed of the orchestra. We play for trillions.",
    "sebastian": "Architecture is the art of planning for change without breaking the present.",
    "priya": "God is in the details, but polish is what makes them sing.",
    "vigil": "Truth is the only foundation that doesn't crumble under scale.",
    "rowan": "Depth is the difference between a project and a legacy.",
    "luna": "Compliance is the shield that allows innovation to move at high velocity.",
    "terry": "Hitting the double when it matters most is all that counts.",
}

def get_agent_data(handle, content):
    data = {}
    
    h1_match = re.search(r'^#\s+(.*?)\s+-\s+Agent Profile', content, re.M | re.I)
    if h1_match: data['human_name'] = h1_match.group(1).strip()
    
    quote_match = re.search(r'>\s*(_|")*(.*?)(_|")*', content, re.M)
    if quote_match and "Creed" not in quote_match.group(2) and "Profile" not in quote_match.group(2):
        data['quote'] = quote_match.group(2).strip().strip('"').strip('_')

    # Extract whole blocks
    blocks = content.split('\n## ')
    sections = ["Capabilities", "Standard Operating Procedures", "Personality", "Restrictions", "Learning Log", "Performance Metrics", "Collaboration", "Tools & Resources", "Specializations"]
    for section in sections:
        for block in blocks:
            # Match start of block precisely
            if block.lower().strip().startswith(section.lower()):
                lines = block.splitlines()
                if len(lines) > 1:
                    text = '\n'.join(lines[1:]).strip()
                    # Clean up trailing separators
                    text = re.split(r'\n---', text)[0].strip()
                    if text and not re.search(r'^\[?Pending initialization', text, re.I):
                        data[section.lower().replace(" ", "_") + '_raw'] = text
                break

    return data

def upgrade_skill(agent_handle, skill_path):
    print(f"Upgrading @{agent_handle}...")
    content = skill_path.read_text(encoding='utf-8')
    existing_data = get_agent_data(agent_handle, content)
    meta = AGENT_META.get(agent_handle, (agent_handle.capitalize(), agent_handle.capitalize(), "Specialist", "General"))
    
    template_content = TEMPLATE_PATH.read_text(encoding='utf-8')
    new_content = template_content
    
    # Fill Metadata
    new_content = re.sub(r'name: \[agent-handle\]', f'name: @{agent_handle}', new_content)
    new_content = re.sub(r'description: \[Short summary of value proposition\]', f'description: {meta[2]}', new_content)
    new_content = re.sub(r'tier: \[Command/Development/Growth/Intel/Automation/Legal\]', f'tier: {meta[3]}', new_content)
    new_content = re.sub(r'# \[Human Name\] - Agent Profile', f'# {meta[0]} - Agent Profile', new_content)
    
    quote = existing_data.get('quote', DEFAULT_QUOTES.get(agent_handle, f"Excellence is not an act, but a habit. @{agent_handle} is always ready."))
    new_content = re.sub(r'> \*\"\[Philosophy Quote - One line that defines this agent\'s approach\]\"\*', f'> "{quote}"', new_content)
    
    new_content = re.sub(r'@\[handle\]', f'@{agent_handle}', new_content)
    new_content = re.sub(r'\[Full Name\]', meta[0], new_content)
    new_content = re.sub(r'\[The Nickname\]', meta[1], new_content)
    new_content = re.sub(r'\[Primary Role Description\]', meta[2], new_content)
    
    authority = "L3 (Strategic)" if meta[3] == "Command" else "L2 (Operational)"
    hue = (hash(agent_handle) % 360)
    new_content = re.sub(r'L\[1-4\] \(\[Tactical/Operational/Strategic/Critical\]\)', authority, new_content)
    new_content = re.sub(r'hsl\(\[h\], \[s\]%, \[l\]%\) - \[Color Name\]', f'hsl({hue}, 70%, 50%) - Agent Color', new_content)

    # Inject Sections (including Specializations)
    sections = [
        ("Capabilities", "capabilities"),
        ("Standard Operating Procedures", "standard_operating_procedures"),
        ("Personality", "personality"),
        ("Restrictions", "restrictions"),
        ("Learning Log", "learning_log"),
        ("Performance Metrics", "performance_metrics"),
        ("Collaboration", "collaboration"),
        ("Tools & Resources", "tools_&_resources")
    ]
    
    for section_name, data_key in sections:
        old_raw = existing_data.get(data_key + '_raw')
        if old_raw:
            # Be very careful with replacement to avoid duplicates
            pattern = re.compile(rf"## {section_name}.*?---", re.S)
            replacement = lambda m: f"## {section_name}\n\n{old_raw}\n\n---"
            new_content = pattern.sub(replacement, new_content)

    # Clean remaining placeholders
    new_content = re.sub(r'\[.*?\]', "Pending initialization...", new_content)
    new_content = re.sub(r'YYYY-MM-DD', '2026-02-19', new_content)

    skill_path.write_text(new_content, encoding='utf-8')

def main():
    for agent_dir in sorted(SKILLS_DIR.iterdir()):
        if agent_dir.is_dir() and agent_dir.name != "methodology":
            skill_file = agent_dir / "SKILL.md"
            if skill_file.exists():
                upgrade_skill(agent_dir.name, skill_file)

if __name__ == "__main__":
    main()
