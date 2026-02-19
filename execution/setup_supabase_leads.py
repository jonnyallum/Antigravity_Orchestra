
import os
import psycopg2
from dotenv import load_dotenv

def create_leads_table():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\Insydetradar\Insydetradar\.env"
    load_dotenv(env_path)
    
    db_url = os.getenv("DATABASE_URL")
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Create leads table for the landing page
        sql = """
        CREATE TABLE IF NOT EXISTS leads (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Enable RLS
        ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
        
        -- Allow anonymous inserts
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_policies WHERE tablename = 'leads' AND policyname = 'Allow anonymous inserts'
            ) THEN
                CREATE POLICY "Allow anonymous inserts" ON leads FOR INSERT WITH CHECK (true);
            END IF;
        END $$;
        """
        cur.execute(sql)
        conn.commit()
        print("Table 'leads' verified/created and RLS configured.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    create_leads_table()
