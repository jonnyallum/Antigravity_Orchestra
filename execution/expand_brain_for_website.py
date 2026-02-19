
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def expand_schema():
    conn = psycopg2.connect(connection_string)
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
            agent_id TEXT REFERENCES agents(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("Schema expanded successfully.")

if __name__ == "__main__":
    expand_schema()
