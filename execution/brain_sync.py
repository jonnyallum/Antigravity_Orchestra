
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Configuration
CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")
ROOT_DIR = Path(__file__).parent.parent
MEMORY_DIR = ROOT_DIR / ".agent" / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
SESSIONS_DIR = MEMORY_DIR / "sessions"

def get_db():
    return psycopg2.connect(CONNECTION_STRING)

def sync_learnings():
    """Push local learnings to Supabase."""
    print("Syncing learnings to Shared Brain...")
    if not LEARNINGS_DIR.exists():
        print("No local learnings found.")
        return

    conn = get_db()
    cur = conn.cursor()

    # ── Detect actual column names in the learnings table ──────────────────────
    try:
        cur.execute("SELECT * FROM learnings LIMIT 1;")
        colnames = [desc[0] for desc in cur.description]
        print(f"  Learnings table columns: {colnames}")
    except Exception as e:
        print(f"  Could not inspect learnings table: {e}")
        conn.rollback()
        cur.close()
        conn.close()
        return

    agent_col   = next((c for c in ["source_agent", "agent_handle", "agent", "agent_id"] if c in colnames), None)
    content_col = next((c for c in ["learning", "content", "text"] if c in colnames), None)
    time_col    = next((c for c in ["created_at", "timestamp", "synced_at"] if c in colnames), None)

    if not agent_col or not content_col:
        print(f"  Cannot map columns — agent_col={agent_col}, content_col={content_col}. Aborting learnings sync.")
        conn.rollback()
        cur.close()
        conn.close()
        return

    print(f"  Using: agent={agent_col}, content={content_col}, time={time_col}")

    for agent_file in LEARNINGS_DIR.glob("*.json"):
        agent_handle = agent_file.stem
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entry in data.get("learnings", []):
                ts = entry.get('timestamp', datetime.now().isoformat())
                if time_col:
                    cur.execute(f"""
                        INSERT INTO learnings ({agent_col}, {content_col}, {time_col})
                        VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (agent_handle, entry['learning'], ts))
                else:
                    cur.execute(f"""
                        INSERT INTO learnings ({agent_col}, {content_col})
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (agent_handle, entry['learning']))

        except Exception as e:
            print(f"  Error syncing {agent_handle}: {e}")
            conn.rollback()
            conn = get_db()
            cur = conn.cursor()

    conn.commit()
    cur.close()
    conn.close()
    print("Learning sync complete.")

def sync_heartbeat():
    """Standard heartbeat check and agent activity log for the entire orchestra."""
    print("Checking orchestra heartbeat...")
    
    # Metadata map for all 42 agents from Jai.OS 4.0 roster
    # Format: handle: (human_name, nickname, role, tier)
    agent_meta = {
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
    
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Mark all agents as active with latest sync
        for handle, (name, nickname, role, tier) in agent_meta.items():
            cur.execute("""
                INSERT INTO agents (id, human_name, nickname, role, tier, status, last_active)
                VALUES (%s, %s, %s, %s, %s, 'active', NOW())
                ON CONFLICT (id) DO UPDATE 
                SET status = 'active', last_active = NOW(), human_name = EXCLUDED.human_name, 
                    nickname = EXCLUDED.nickname, role = EXCLUDED.role, tier = EXCLUDED.tier;
            """, (handle, name, nickname, role, tier))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"Heartbeat sync successful for {len(agent_meta)} agents.")
    except Exception as e:
        print(f"Heartbeat sync error: {e}")

def pull_learnings():
    """Pull global learnings from Supabase to local memory."""
    print("Pulling global learnings from Shared Brain...")
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Get all learnings from the last 7 days
        print(f"Executing query on table 'learnings'...")
        cur.execute("""
            SELECT * FROM learnings LIMIT 1;
        """)
        colnames = [desc[0] for desc in cur.description]
        print(f"Detected columns: {colnames}")
        
        target_col = "source_agent" if "source_agent" in colnames else "agent_handle" if "agent_handle" in colnames else "agent"
        content_col = "learning" if "learning" in colnames else "content"
        print(f"Using columns: {target_col}, {content_col}")

        cur.execute(f"""
            SELECT {target_col}, {content_col}, created_at 
            FROM learnings 
            WHERE created_at > NOW() - INTERVAL '7 days'
            ORDER BY created_at DESC;
        """)
        
        rows = cur.fetchall()
        if not rows:
            print("No new global learnings found.")
            return

        # Group by agent
        agent_data = {}
        for agent_id, content, created_at in rows:
            if agent_id not in agent_data:
                agent_data[agent_id] = []
            agent_data[agent_id].append({
                "learning": content,
                "timestamp": created_at.isoformat() if hasattr(created_at, 'isoformat') else str(created_at),
                "source": "shared_brain"
            })

        # Save to local memory
        LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
        for agent_id, learnings in agent_data.items():
            agent_file = LEARNINGS_DIR / f"{agent_id}.json"
            
            # Load existing or create new
            if agent_file.exists():
                with open(agent_file, 'r', encoding='utf-8') as f:
                    local_data = json.load(f)
            else:
                local_data = {"agent": agent_id, "learnings": [], "tasks": [], "patterns": {}}

            # Merge learnings (avoiding exact duplicates)
            existing_contents = [l["learning"] for l in local_data.get("learnings", [])]
            new_added = 0
            for l in learnings:
                if l["learning"] not in existing_contents:
                    local_data["learnings"].append(l)
                    new_added += 1
            
            if new_added > 0:
                with open(agent_file, 'w', encoding='utf-8') as f:
                    json.dump(local_data, f, indent=2)
                print(f"Propagated {new_added} learnings to @{agent_id}")

        cur.close()
        conn.close()
        print("Pull sync complete.")
    except Exception as e:
        print(f"Pull sync error: {e}")

if __name__ == "__main__":
    if "--pull" in sys.argv:
        pull_learnings()
    else:
        sync_heartbeat()
        sync_learnings()
