
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def verify_migration_002():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        # Check columns in agents
        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'agents' AND column_name IN ('philosophy', 'personality', 'tier', 'featured', 'avatar')")
        cols = [c[0] for c in cur.fetchall()]
        print(f"Agent columns: {cols}")
        
        # Check system_news table
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'system_news'")
        news_table = cur.fetchone()
        print(f"System News table: {'Exists' if news_table else 'Missing'}")
        
        # Check trigger function
        cur.execute("SELECT routine_name FROM information_schema.routines WHERE routine_name = 'set_next_task_run'")
        trigger_func = cur.fetchone()
        print(f"Trigger function 'set_next_task_run': {'Exists' if trigger_func else 'Missing'}")
        
        if not trigger_func:
            print("Injecting trigger function...")
            cur.execute("""
                CREATE OR REPLACE FUNCTION set_next_task_run()
                RETURNS TRIGGER AS $func$
                BEGIN
                    IF NEW.is_recurring = true AND NEW.status = 'completed' AND OLD.status != 'completed' THEN
                        UPDATE tasks SET next_run_at = NOW() + INTERVAL '1 day' WHERE id = NEW.id;
                    END IF;
                    RETURN NEW;
                END;
                $func$ LANGUAGE plpgsql;
            """)
            cur.execute("DROP TRIGGER IF EXISTS trigger_task_recurring ON tasks;")
            cur.execute("""
                CREATE TRIGGER trigger_task_recurring
                AFTER UPDATE ON tasks
                FOR EACH ROW
                EXECUTE FUNCTION set_next_task_run();
            """)
            conn.commit()
            print("Trigger injected successfully.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_migration_002()
