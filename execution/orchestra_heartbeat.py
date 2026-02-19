
import os
import time
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# We'll use the environment variable for the brain
# If direct connection fails (IPv6 issue), we'll log it and suggest local bridge
CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

class ResearchHeartbeat:
    """The heartbeat of the Orchestra's autonomous research loop."""
    
    def __init__(self):
        self.interval = 60 # Check every minute
        self.active = True

    def check_scheduled_tasks(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for scheduled research tasks...")
        try:
            # Note: We need a way to parse CRON expressions if we want high precision.
            # For now, we'll check next_run_at <= NOW()
            conn = psycopg2.connect(CONNECTION_STRING)
            cur = conn.cursor()
            
            # 1. Find master tasks due for execution
            cur.execute("""
                SELECT id, title, description, assigned_to, project_id 
                FROM tasks 
                WHERE is_recurring = true 
                AND status = 'pending' 
                AND (next_run_at <= NOW() OR next_run_at IS NULL)
            """)
            
            due_tasks = cur.fetchall()
            
            for master_id, title, desc, agent_id, project_id in due_tasks:
                print(f"!!! TRIGGERING RESEARCH: {title} for {agent_id}")
                
                # Clone into an execution instance
                cur.execute("""
                    INSERT INTO tasks (title, description, assigned_to, project_id, status, parent_task_id, created_by_ai)
                    VALUES (%s, %s, %s, %s, 'pending', %s, 'heartbeat')
                    RETURNING id;
                """, (f"RUN: {title} ({datetime.now().strftime('%Y-%m-%d')})", desc, agent_id, project_id, master_id))
                
                new_task_id = cur.fetchone()[0]
                
                # Update master schedule (Mock cron: 24h later)
                cur.execute("""
                    UPDATE tasks 
                    SET next_run_at = NOW() + INTERVAL '24 hours' 
                    WHERE id = %s;
                """, (master_id,))
                
                # Log to News Feed (Automatic Website Update)
                cur.execute("""
                    INSERT INTO system_news (title, content, type, agent_id)
                    VALUES (%s, %s, 'milestone', %s);
                """, (f"Autonomous Research: {title}", f"Agent {agent_id} has been deployed for a scheduled research run.", agent_id))

            conn.commit()
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"Heartbeat Error: {e}")
            if "could not translate host name" in str(e):
                print(">>> CRITICAL: Your local machine cannot reach the Supabase DB via IPv6.")
                print(">>> FIX: Use the Supabase Pooler URI or run migrations in the Supabase Dashboard.")
                self.active = False # Stop loop if we can't connect

    def run(self):
        print("--- Antigravity Heartbeat Active ---")
        while self.active:
            self.check_scheduled_tasks()
            time.sleep(self.interval)

if __name__ == "__main__":
    beat = ResearchHeartbeat()
    beat.run()
