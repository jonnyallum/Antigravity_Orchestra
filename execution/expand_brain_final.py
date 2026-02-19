
import psycopg2
import os
import urllib.parse as urlparse
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def expand_schema():
    print(f"Connecting to: {connection_string.split('@')[-1]}") # Log host only for safety
    try:
        # Use explicit parameters instead of URI to avoid parsing issues
        url = urlparse.urlparse(connection_string)
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
            sslmode='require'
        )
        cur = conn.cursor()
        
        # 1. Expand agents table
        print("Expanding agents table...")
        cur.execute("""
            ALTER TABLE agents 
            ADD COLUMN IF NOT EXISTS philosophy TEXT,
            ADD COLUMN IF NOT EXISTS personality TEXT[] DEFAULT '{}',
            ADD COLUMN IF NOT EXISTS tier TEXT DEFAULT 'development',
            ADD COLUMN IF NOT EXISTS featured BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS avatar TEXT;
        """)
        
        # 2. Create system_news table
        print("Creating system_news table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS system_news (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                type TEXT DEFAULT 'update', -- news | update | hiring | milestone
                is_active BOOLEAN DEFAULT true,
                agent_id TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        
        # 3. Expand tasks table for cron
        print("Expanding tasks table for scheduling...")
        cur.execute("""
            ALTER TABLE tasks 
            ADD COLUMN IF NOT EXISTS cron_expression TEXT,
            ADD COLUMN IF NOT EXISTS next_run_at TIMESTAMPTZ,
            ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS parent_task_id UUID;
        """)
        
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_next_run ON tasks(next_run_at) WHERE is_recurring = true;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Schema expanded successfully (Jai.OS 4.0 Research Cron Ready).")
    except Exception as e:
        print(f"Error expanding schema: {e}")

if __name__ == "__main__":
    expand_schema()
