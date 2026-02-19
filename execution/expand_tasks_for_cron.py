
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def expand_tasks_for_cron():
    # Fix the connection string for psycopg2 (if it has @ and symbols)
    # The error before was "could not translate host name", let's verify connectivity first
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        
        print("Expanding tasks table for scheduling...")
        cur.execute("""
            ALTER TABLE tasks 
            ADD COLUMN IF NOT EXISTS cron_expression TEXT,
            ADD COLUMN IF NOT EXISTS next_run_at TIMESTAMPTZ,
            ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS parent_task_id UUID; -- Link occurrences to master schedule
        """)
        
        # Create an index for next_run_at for fast polling
        print("Creating index for task scheduling...")
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_next_run ON tasks(next_run_at) WHERE is_recurring = true;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Tasks expanded successfully.")
    except Exception as e:
        print(f"Error expanding tasks: {e}")

if __name__ == "__main__":
    expand_tasks_for_cron()
