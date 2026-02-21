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

def aggregate_wins():
    print("💰 AGGREGATING AGENCY WINS...")
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        # Pull recent completed tasks marked as "success"
        cur.execute("""
            SELECT title, agent_id 
            FROM tasks 
            WHERE status = 'completed' 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        
        wins = cur.fetchall()
        
        if not wins:
            print("No recent wins found in the brain.")
            return

        print("\n--- LIVE AGENCY STATS ---")
        for title, agent in wins:
            print(f"✅ mission accomplished: {title} (@{agent})")
            
        print("\n🎨 COMPONENT GENERATION READY: Use @Priya to hydrate 'StatsGrid.tsx'")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Aggregator Error: {e}")

if __name__ == "__main__":
    aggregate_wins()
