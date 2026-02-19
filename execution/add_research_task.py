
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def add_competitor_watch():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        # Add a recurring research task for Sophie (Scout)
        print("Adding 'Competitor Watch' recurring task for @Scout...")
        cur.execute("""
            INSERT INTO tasks (
                title, 
                description, 
                assigned_to, 
                priority, 
                status, 
                is_recurring, 
                cron_expression, 
                next_run_at, 
                created_by_ai
            )
            VALUES (
                'Daily Competitor Intel', 
                'Scan for new features or pricing changes from primary competitors in the AI Venture space.', 
                'sophie', 
                'P1', 
                'pending', 
                true, 
                '0 9 * * *', 
                NOW(), 
                'claude'
            )
            RETURNING id;
        """)
        
        task_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        print(f"Success! Master Task ID: {task_id}")
        print("The 'Heartbeat' script will now see this task and trigger it.")
    except Exception as e:
        print(f"Error adding task: {e}")

if __name__ == "__main__":
    add_competitor_watch()
