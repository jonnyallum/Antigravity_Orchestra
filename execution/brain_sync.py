#!/usr/bin/env python3
"""
Antigravity Orchestra - Brain Sync Protocol
Syncs local learnings, agent health, and session data to the Supabase Shared Brain.

Supabase 'learnings' table schema:
  id (uuid), source_agent (text FK->agents.id), source_task_id (uuid),
  source_project (text), source_ai (text), learning (text), category (text),
  tags (text[]), propagate_to (text[]), applied_count (int), verified (bool),
  verified_by (text), created_at (timestamptz)

Supabase 'agents' table schema:
  id (text PK), human_name (text), nickname (text), role (text), status (text),
  current_ai (text), last_active (timestamptz), capabilities (text[]),
  authority_level (int), learning_count (int), task_count (int),
  success_rate (numeric), philosophy (text), personality (text[]),
  tier (text), featured (bool), avatar (text)

@Owner: @Marcus (The Maestro)
@Created: 2026-02-01
@Updated: 2026-02-11 (Fixed schema mismatch, added auto-register, savepoints)
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")
ROOT_DIR = Path(__file__).parent.parent
MEMORY_DIR = ROOT_DIR / ".agent" / "memory"
LEARNINGS_DIR = MEMORY_DIR / "learnings"
SKILLS_DIR = ROOT_DIR / ".agent" / "skills"


def get_db():
    if not CONNECTION_STRING:
        raise ValueError("ANTIGRAVITY_BRAIN_CONNECTION_STRING not set in .env")
    return psycopg2.connect(CONNECTION_STRING)


def get_supabase_agent_ids(cur):
    """Get set of agent IDs currently in Supabase."""
    cur.execute("SELECT id FROM agents")
    return {row[0] for row in cur.fetchall()}


def extract_agent_meta(skill_path):
    """Extract human_name, nickname, role from a SKILL.md file."""
    try:
        content = skill_path.read_text(encoding="utf-8")
        human_name = ""
        nickname = ""
        role = ""
        for line in content.split("\n")[:30]:
            if "Human Name" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    human_name = parts[2].strip().strip("*")
            if "Nickname" in line and "|" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    nickname = parts[2].strip().strip('"').strip("*")
            if "Role" in line and "|" in line and "role" not in line.lower().split("|")[0].lower().replace("role",""):
                parts = line.split("|")
                if len(parts) >= 3:
                    role = parts[2].strip().strip("*")
        # Fallback: extract from first heading
        if not human_name:
            m = re.search(r"^#\s+@\w+\s*[-—]\s*(.+?)(?:\"|$)", content, re.MULTILINE)
            if m:
                human_name = m.group(1).strip().strip('"')
        return human_name, nickname, role
    except Exception:
        return "", "", ""


def sync_missing_agents():
    """Register any local agents missing from Supabase."""
    print("Checking for missing agents in Supabase...")
    conn = get_db()
    cur = conn.cursor()
    
    existing = get_supabase_agent_ids(cur)
    excludes = {"methodology"}
    registered = 0
    
    for agent_dir in sorted(SKILLS_DIR.iterdir()):
        if not agent_dir.is_dir() or agent_dir.name in excludes:
            continue
        skill_file = agent_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        handle = agent_dir.name
        if handle in existing:
            continue
        
        human_name, nickname, role = extract_agent_meta(skill_file)
        
        try:
            cur.execute("""
                INSERT INTO agents (id, human_name, nickname, role, status, last_active, 
                                    authority_level, learning_count, task_count, success_rate,
                                    tier, featured, created_at, updated_at)
                VALUES (%s, %s, %s, %s, 'active', NOW(), 2, 0, 0, 0.0, 
                        'core', false, NOW(), NOW())
                ON CONFLICT (id) DO NOTHING;
            """, (handle, human_name or handle, nickname or "", role or "Specialist"))
            registered += 1
            print(f"  + Registered @{handle} ({human_name or handle})")
        except Exception as e:
            print(f"  Error registering @{handle}: {e}")
            conn.rollback()
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"  Registered {registered} new agents.")
    return registered


def sync_learnings():
    """Push local learnings to Supabase Shared Brain.
    
    Uses savepoints so one failure doesn't abort the whole batch.
    """
    print("Syncing learnings to Shared Brain...")
    
    conn = get_db()
    cur = conn.cursor()
    
    # Get valid agent IDs
    valid_agents = get_supabase_agent_ids(cur)
    
    synced = 0
    skipped = 0
    errors = 0
    dupes = 0

    # Source 1: JSON learning files in memory/learnings/
    if LEARNINGS_DIR.exists():
        for agent_file in LEARNINGS_DIR.glob("*.json"):
            agent_handle = agent_file.stem
            if agent_handle not in valid_agents:
                skipped += 1
                continue
            
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for entry in data.get("learnings", []):
                    learning_text = entry.get('learning', entry.get('content', ''))
                    if not learning_text:
                        continue
                    
                    timestamp = entry.get('timestamp', datetime.now().isoformat())
                    category = entry.get('category', 'general')
                    tags = entry.get('tags', [])
                    project = entry.get('project', '')
                    
                    try:
                        cur.execute("SAVEPOINT sp_learning")
                        cur.execute("SELECT 1 FROM learnings WHERE source_agent=%s AND learning=%s LIMIT 1", (agent_handle, learning_text))
                        if cur.fetchone() is None:
                            cur.execute("""
                                INSERT INTO learnings (source_agent, source_ai, learning, category, created_at, applied_count, verified)
                                VALUES (%s, %s, %s, %s, %s, 0, false);
                            """, (agent_handle, 'cline', learning_text, category, timestamp))
                            synced += 1
                        else:
                            dupes += 1
                        cur.execute("RELEASE SAVEPOINT sp_learning")
                    except Exception as e:
                        cur.execute("ROLLBACK TO SAVEPOINT sp_learning")
                        if errors < 3:
                            print(f"  Err [{agent_handle}]: {e}")
                        errors += 1
                    
            except Exception as e:
                print(f"  Error reading {agent_handle}: {e}")
                errors += 1

    # Source 2: Extract learnings from SKILL.md files
    if SKILLS_DIR.exists():
        excludes = {"methodology"}
        for agent_dir in SKILLS_DIR.iterdir():
            if not agent_dir.is_dir() or agent_dir.name in excludes:
                continue
            
            skill_file = agent_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            
            agent_handle = agent_dir.name
            if agent_handle not in valid_agents:
                skipped += 1
                continue
            
            try:
                content = skill_file.read_text(encoding='utf-8')
                
                in_learning = False
                for line in content.split('\n'):
                    lower = line.lower().strip()
                    if 'learning log' in lower or 'learning_log' in lower:
                        in_learning = True
                        continue
                    if in_learning and line.strip().startswith('## '):
                        break
                    if in_learning and line.strip().startswith('- ') and len(line.strip()) > 10:
                        learning_text = line.strip().lstrip('- ').strip()
                        if learning_text and not learning_text.startswith('(No entries'):
                            try:
                                cur.execute("SAVEPOINT sp_skill")
                                cur.execute("SELECT 1 FROM learnings WHERE source_agent=%s AND learning=%s LIMIT 1", (agent_handle, learning_text))
                                if cur.fetchone() is None:
                                    cur.execute("""
                                        INSERT INTO learnings (source_agent, source_ai, learning, category, created_at, applied_count, verified)
                                        VALUES (%s, %s, %s, %s, NOW(), 0, false);
                                    """, (agent_handle, 'cline', learning_text, 'skill-log'))
                                    synced += 1
                                else:
                                    dupes += 1
                                cur.execute("RELEASE SAVEPOINT sp_skill")
                            except Exception as e:
                                cur.execute("ROLLBACK TO SAVEPOINT sp_skill")
                                if errors < 3:
                                    print(f"  Err [{agent_handle}]: {e}")
                                errors += 1
            except Exception as e:
                print(f"  Error extracting from {agent_dir.name}: {e}")
                errors += 1

    conn.commit()
    cur.close()
    conn.close()
    
    print(f"  Synced: {synced} | Dupes: {dupes} | Skipped: {skipped} | Errors: {errors}")
    print("Learning sync complete.")


def sync_heartbeat():
    """Standard heartbeat check."""
    print("Checking orchestra heartbeat...")
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE agents SET status = 'active', last_active = NOW() 
            WHERE id = 'marcus';
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("  Heartbeat: OK")
    except Exception as e:
        print(f"  Heartbeat error: {e}")


def sync_agent_health():
    """Push local agent-health.json to Supabase agents table."""
    print("Syncing agent health...")
    health_file = MEMORY_DIR / "agent-health.json"
    if not health_file.exists():
        print("  No agent-health.json found.")
        return
    
    try:
        with open(health_file, 'r', encoding='utf-8') as f:
            health = json.load(f)
        
        conn = get_db()
        cur = conn.cursor()
        valid = get_supabase_agent_ids(cur)
        
        agents = health.get("agents", health)
        updated = 0
        if isinstance(agents, dict):
            for handle, metrics in agents.items():
                if handle in valid and isinstance(metrics, dict):
                    cur.execute("""
                        UPDATE agents SET status = 'active', last_active = NOW(), updated_at = NOW()
                        WHERE id = %s;
                    """, (handle,))
                    updated += 1
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"  Updated {updated} agents.")
    except Exception as e:
        print(f"  Health sync error: {e}")


if __name__ == "__main__":
    sync_heartbeat()
    sync_missing_agents()
    sync_learnings()
    sync_agent_health()
