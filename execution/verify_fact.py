import sys
import io

# Force UTF-8 for stdout/stderr
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def add_fact(project_id, key, value, category, agent_handle):
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO verified_facts (project_id, key, value, category, verified_by_ai)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (project_id, key) 
            DO UPDATE SET value = EXCLUDED.value, verified_at = NOW(), verified_by_ai = EXCLUDED.verified_by_ai;
        """, (project_id, key, value, category, agent_handle))
        
        conn.commit()
        print(f"✅ FACT LOCKED: {key} = {value} (Category: {category})")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error locking fact: {e}")

def get_facts(project_id):
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        cur.execute("SELECT key, value, category FROM verified_facts WHERE project_id = %s", (project_id,))
        facts = cur.fetchall()
        
        if not facts:
            print("No verified facts found for this project.")
        else:
            print(f"--- TRUTH-LOCK: PROJECT {project_id} ---")
            for key, val, cat in facts:
                print(f"[{cat}] {key}: {val}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error retrieving facts: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_fact.py [list|add] [project_id] [key] [value] [category] [agent]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "list":
        get_facts(sys.argv[2])
    elif cmd == "add":
        add_fact(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
