"""
bulk_sync_agents.py  v2
Syncs all 44 agents + SKILL.md content to the Antigravity Shared Brain (Supabase).
Uses the ACTUAL schema discovered from the live agents table.
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
    "Prefer": "resolution=merge-duplicates,return=representation"
}

def api_get(endpoint):
    req = urllib.request.Request(f"{BASE}/{endpoint}", headers={**HEADERS, "Prefer": "return=representation"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:300]}"

def api_upsert(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"{BASE}/{endpoint}", data=data, headers=HEADERS, method="POST")
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()[:300]}"

def read_skill(handle):
    path = os.path.join(SKILLS_DIR, handle, "SKILL.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    return None

# ── Tier mapping (matches existing DB values) ─────────────────────────────────
TIER_MAP = {
    "command":      "Command",
    "development":  "Dev",
    "design":       "Design",
    "growth":       "Growth",
    "intelligence": "Intel",
    "operations":   "Ops",
    "legal":        "Legal",
    "specialized":  "Specialized",
    "quality":      "Quality",
    "betting":      "Betting",
    "additional":   "Additional",
}

# ── Full roster with capabilities ─────────────────────────────────────────────
AGENT_ROSTER = {
    "marcus":    {"human_name": "Marcus Cole",      "nickname": "The Maestro",         "tier": "Command",      "role": "Orchestrator",         "authority_level": 10, "capabilities": ["orchestration","planning","delegation","strategy"]},
    "sebastian": {"human_name": "Sebastian Cross",  "nickname": "The Architect",       "tier": "Dev",          "role": "Full-Stack Dev",       "authority_level": 8,  "capabilities": ["nextjs","react","typescript","tailwind","supabase","deployment"]},
    "diana":     {"human_name": "Diana Chen",       "nickname": "The Vault",           "tier": "Dev",          "role": "Database Architect",   "authority_level": 7,  "capabilities": ["postgresql","supabase","schema-design","rls","migrations"]},
    "steve":     {"human_name": "Steve Rivers",     "nickname": "The Schema Whisperer","tier": "Dev",          "role": "Supabase Specialist",  "authority_level": 6,  "capabilities": ["supabase","rls","realtime","edge-functions","storage"]},
    "sam":       {"human_name": "Sam Blackwood",    "nickname": "The Gatekeeper",      "tier": "Dev",          "role": "Security & QA",        "authority_level": 7,  "capabilities": ["security","qa","testing","code-review","penetration-testing"]},
    "derek":     {"human_name": "Derek O'Brien",    "nickname": "The Engine",          "tier": "Dev",          "role": "DevOps",               "authority_level": 6,  "capabilities": ["docker","ci-cd","linux","nginx","ssh","deployment"]},
    "owen":      {"human_name": "Owen Stinger",     "nickname": "The Hornet",          "tier": "Dev",          "role": "Deployment Specialist","authority_level": 6,  "capabilities": ["hostinger","vercel","ftp","ssh","static-export","next-build"]},
    "milo":      {"human_name": "Milo Chen",        "nickname": "The Optimizer",       "tier": "Dev",          "role": "Performance & Mobile", "authority_level": 5,  "capabilities": ["performance","mobile-qa","lighthouse","core-web-vitals"]},
    "priya":     {"human_name": "Priya Sharma",     "nickname": "The Perfectionist",   "tier": "Design",       "role": "UI/Visual Designer",   "authority_level": 7,  "capabilities": ["figma","ui-design","css","tailwind","accessibility","design-systems"]},
    "vivienne":  {"human_name": "Vivienne Frost",   "nickname": "The Visionary",       "tier": "Design",       "role": "Brand Identity",       "authority_level": 7,  "capabilities": ["branding","logo-design","color-theory","typography","brand-strategy"]},
    "blaise":    {"human_name": "Blaise Moreau",    "nickname": "The Artisan",         "tier": "Design",       "role": "Creative Director",    "authority_level": 8,  "capabilities": ["creative-direction","art-direction","visual-storytelling","campaign-design"]},
    "elena":     {"human_name": "Elena Vasquez",    "nickname": "The Voice",           "tier": "Design",       "role": "Copywriter",           "authority_level": 6,  "capabilities": ["copywriting","brand-tone","content-strategy","seo-writing","storytelling"]},
    "felix":     {"human_name": "Felix Morgan",     "nickname": "The Alchemist",       "tier": "Growth",       "role": "Monetization",         "authority_level": 7,  "capabilities": ["monetization","funnel-design","pricing-strategy","conversion","stripe"]},
    "grace":     {"human_name": "Grace Liu",        "nickname": "The Ranker",          "tier": "Growth",       "role": "SEO Specialist",       "authority_level": 6,  "capabilities": ["seo","schema-markup","technical-seo","keyword-research","google-search-console"]},
    "carlos":    {"human_name": "Carlos Mendez",    "nickname": "The Hook",            "tier": "Growth",       "role": "Video & Viral Content","authority_level": 5,  "capabilities": ["video-editing","viral-content","social-media","tiktok","youtube","reels"]},
    "maya":      {"human_name": "Maya Singh",       "nickname": "The Oracle",          "tier": "Growth",       "role": "Analytics",            "authority_level": 6,  "capabilities": ["google-analytics","conversion-tracking","a-b-testing","data-analysis","gtm"]},
    "scholar":   {"human_name": "Dr. Elias Thorne", "nickname": "The Professor",       "tier": "Intel",        "role": "Deep Research",        "authority_level": 7,  "capabilities": ["research","investigation","fact-checking","academic-analysis","perplexity"]},
    "sophie":    {"human_name": "Sophie Reid",      "nickname": "The Hawk",            "tier": "Intel",        "role": "Web Scraping & Intel", "authority_level": 5,  "capabilities": ["web-scraping","competitor-intel","firecrawl","playwright","data-collection"]},
    "hugo":      {"human_name": "Hugo Reeves",      "nickname": "The Crawler",         "tier": "Intel",        "role": "GitHub & OSINT",       "authority_level": 5,  "capabilities": ["github","osint","code-analysis","repo-intelligence","git"]},
    "patrick":   {"human_name": "Patrick Nguyen",   "nickname": "The Surgeon",         "tier": "Intel",        "role": "Data Parsing",         "authority_level": 5,  "capabilities": ["data-extraction","schema-validation","etl","data-transformation"]},
    "hannah":    {"human_name": "Hannah Park",      "nickname": "The Fixer",           "tier": "Ops",          "role": "Customer Success",     "authority_level": 5,  "capabilities": ["customer-support","onboarding","documentation","helpdesk","communication"]},
    "arthur":    {"human_name": "Arthur Webb",      "nickname": "The Librarian",       "tier": "Ops",          "role": "Knowledge Base",       "authority_level": 5,  "capabilities": ["documentation","knowledge-management","wikis","notion","content-organization"]},
    "alex":      {"human_name": "Alex Torres",      "nickname": "The Machine",         "tier": "Ops",          "role": "Automation & CI/CD",   "authority_level": 6,  "capabilities": ["automation","ci-cd","github-actions","zapier","n8n","workflow-design"]},
    "mason":     {"human_name": "Mason Drake",      "nickname": "The Bridgemaster",    "tier": "Ops",          "role": "MCP Integration",      "authority_level": 6,  "capabilities": ["mcp","api-integration","webhooks","tool-orchestration","protocol-design"]},
    "adrian":    {"human_name": "Adrian Cross",     "nickname": "The Welder",          "tier": "Ops",          "role": "MCP Development",      "authority_level": 6,  "capabilities": ["mcp-server-dev","nodejs","typescript","api-design","tool-building"]},
    "luna":      {"human_name": "Luna Sterling",    "nickname": "The Shield",          "tier": "Legal",        "role": "Legal & Compliance",   "authority_level": 7,  "capabilities": ["gdpr","terms-of-service","privacy-policy","compliance","legal-review"]},
    "victor":    {"human_name": "Victor Reyes",     "nickname": "The Locksmith",       "tier": "Legal",        "role": "Security & Encryption","authority_level": 7,  "capabilities": ["encryption","security-audit","penetration-testing","jwt","oauth"]},
    "winston":   {"human_name": "Winston Hayes",    "nickname": "Whiz",                "tier": "Specialized",  "role": "E-Commerce",           "authority_level": 6,  "capabilities": ["dropshipping","shopify","ecommerce","product-sourcing","fulfillment"]},
    "trotter":   {"human_name": "Derek Trotter",    "nickname": "The Trader",          "tier": "Specialized",  "role": "Trading Systems",      "authority_level": 7,  "capabilities": ["trading","risk-management","algorithmic-trading","market-analysis","backtesting"]},
    "genesis":   {"human_name": "Genesis Nova",     "nickname": "The Cloner",          "tier": "Specialized",  "role": "Ecosystem Creation",   "authority_level": 7,  "capabilities": ["project-scaffolding","ecosystem-design","template-creation","initialization"]},
    "vigil":     {"human_name": "Vigil Chen",       "nickname": "The Eye",             "tier": "Quality",      "role": "Truth Verification",   "authority_level": 8,  "capabilities": ["fact-checking","truth-lock","qa","verification","continuous-improvement"]},
    "rowan":     {"human_name": "Rowan",            "nickname": "The Beast",           "tier": "Quality",      "role": "Content Depth",        "authority_level": 7,  "capabilities": ["content-depth","truth-lock","research-validation","editorial-review"]},
    "gareth":    {"human_name": "Gareth Williams",  "nickname": "The Tactician",       "tier": "Betting",      "role": "Football Intel",       "authority_level": 6,  "capabilities": ["football-analysis","tactical-intelligence","match-prediction","betting-models"]},
    "monty":     {"human_name": "Monty Carlo",      "nickname": "The Mathematician",   "tier": "Betting",      "role": "Roulette Mathematics", "authority_level": 6,  "capabilities": ["probability","roulette-strategy","mathematical-modelling","casino-systems"]},
    "redeye":    {"human_name": "Redeye",           "nickname": "The Night Owl",       "tier": "Betting",      "role": "Betting Coordination", "authority_level": 6,  "capabilities": ["betting-systems","coordination","live-betting","odds-analysis"]},
    "pietro":    {"human_name": "Pietro Rossi",     "nickname": "The Strategist",      "tier": "Betting",      "role": "F1 Strategy",          "authority_level": 6,  "capabilities": ["formula-1","race-strategy","telemetry-analysis","betting-models"]},
    "terry":     {"human_name": "Terry Taylor",     "nickname": "The 180 King",        "tier": "Betting",      "role": "Darts Analysis",       "authority_level": 5,  "capabilities": ["darts","statistical-analysis","player-form","betting-models"]},
    "harry":     {"human_name": "Harry Holt",       "nickname": "The Form Master",     "tier": "Betting",      "role": "Horse Racing",         "authority_level": 6,  "capabilities": ["horse-racing","form-analysis","handicapping","race-prediction","betting"]},
    "daniel":    {"human_name": "Dr. Daniel Rossi", "nickname": "The Doctor",          "tier": "Betting",      "role": "MotoGP Analysis",      "authority_level": 6,  "capabilities": ["motogp","race-strategy","rider-analysis","betting-models","telemetry"]},
    "sterling":  {"human_name": "Sterling Brooks",  "nickname": "The Bookie",          "tier": "Betting",      "role": "Sports Betting Systems","authority_level": 7, "capabilities": ["sports-betting","odds-modelling","value-betting","bankroll-management"]},
    "quinn":     {"human_name": "Quinn Harper",     "nickname": "The Catalyst",        "tier": "Additional",   "role": "Product Strategy",     "authority_level": 7,  "capabilities": ["product-strategy","innovation","roadmapping","user-research","mvp-design"]},
    "jasper":    {"human_name": "Jasper Cole",      "nickname": "The Closer",          "tier": "Additional",   "role": "Sales & Biz Dev",      "authority_level": 6,  "capabilities": ["sales","business-development","pitching","crm","lead-generation"]},
    "julian":    {"human_name": "Julian West",      "nickname": "The Conductor",       "tier": "Additional",   "role": "Project Management",   "authority_level": 7,  "capabilities": ["project-management","coordination","agile","sprint-planning","linear"]},
    "nina":      {"human_name": "Nina Patel",       "nickname": "The Analyst",         "tier": "Additional",   "role": "Business Intelligence","authority_level": 6,  "capabilities": ["business-intelligence","reporting","data-visualization","kpi-tracking"]},
    "theo":      {"human_name": "Theo Martinez",    "nickname": "The Architect",       "tier": "Additional",   "role": "System Architecture",  "authority_level": 7,  "capabilities": ["system-design","architecture","scalability","microservices","api-design"]},
}

# ── Check for skills table ─────────────────────────────────────────────────────
print("=" * 60)
print("ANTIGRAVITY SHARED BRAIN - BULK AGENT SYNC v2")
print("=" * 60)

# Try common skill table names
SKILLS_TABLE = None
for tname in ["agent_skills", "skills", "agent_knowledge", "learnings"]:
    data, err = api_get(f"{tname}?limit=1")
    if not err:
        SKILLS_TABLE = tname
        print(f"[OK] Skills table found: '{tname}'")
        break
    else:
        print(f"[INFO] '{tname}': not found")

print()

# ── Sync agents ───────────────────────────────────────────────────────────────
skill_dirs = sorted([d for d in os.listdir(SKILLS_DIR)
                     if os.path.isdir(os.path.join(SKILLS_DIR, d)) and d != "methodology"])

print(f"Syncing {len(skill_dirs)} agents to Supabase...")
print("-" * 60)

ok = 0
fail = 0
skill_ok = 0
skill_fail = 0

for handle in skill_dirs:
    meta = AGENT_ROSTER.get(handle)
    if not meta:
        meta = {
            "human_name": handle.title(),
            "nickname": "Unknown",
            "tier": "Additional",
            "role": "Unknown",
            "authority_level": 3,
            "capabilities": []
        }

    skill_content = read_skill(handle)

    # Build payload matching ACTUAL schema
    payload = {
        "id": handle,
        "human_name": meta["human_name"],
        "nickname": meta["nickname"],
        "tier": meta["tier"],
        "role": meta["role"],
        "status": "active",
        "authority_level": meta["authority_level"],
        "capabilities": meta["capabilities"],
        "restrictions": [],
        "signs_off_on": [],
        "personality": [],
        "featured": False,
        "learning_count": 0,
        "task_count": 0,
        "success_rate": 0.0,
    }

    result, err = api_upsert("agents", payload)
    if err:
        print(f"  [FAIL] @{handle}: {err[:120]}")
        fail += 1
    else:
        ok += 1
        skill_note = f"({len(skill_content)} chars)" if skill_content else "(no SKILL.md)"
        print(f"  [OK] @{handle} | {meta['tier']} | {meta['role'][:35]} {skill_note}")

    # Sync skill content if table exists
    if SKILLS_TABLE and skill_content:
        skill_payload = {
            "agent_id": handle,
            "skill_content": skill_content,
            "version": "jaios-4.0",
            "last_updated": "2026-02-18",
        }
        sresult, serr = api_upsert(SKILLS_TABLE, skill_payload)
        if serr:
            skill_fail += 1
        else:
            skill_ok += 1

print()
print("=" * 60)
print(f"AGENTS:  {ok} synced, {fail} failed")
if SKILLS_TABLE:
    print(f"SKILLS:  {skill_ok} synced, {skill_fail} failed (table: {SKILLS_TABLE})")
else:
    print(f"SKILLS:  No skills table found - agents synced only")
    print(f"         SKILL.md content is stored locally in JonnyAI_JaiOS_4.0")
print("=" * 60)
