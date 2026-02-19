
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def check_task_schedule():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        cur.execute("SELECT title, next_run_at, status FROM tasks WHERE is_recurring = true")
        tasks = cur.fetchall()
        
        print("\n--- Recurring Task Schedule ---")
        for title, next_run_at, status in tasks:
            print(f"Task: {title}")
            print(f"Next Run: {next_run_at}")
            print(f"Status: {status}\n")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_task_schedule()
