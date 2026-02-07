
import psycopg2
import os
from dotenv import load_dotenv

def apply_kwizz_schema():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.env"
    load_dotenv(env_path)
    
    conn_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")
    if not conn_string:
        print("Missing ANTIGRAVITY_BRAIN_CONNECTION_STRING")
        return

    # Using absolute path for Jai.OS 4.0 compliance
    sql_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\kwizz\supabase_monetization_schema.sql"
    
    if not os.path.exists(sql_path):
        print(f"SQL file not found at {sql_path}")
        return

    with open(sql_path, 'r') as f:
        sql = f.read()

    try:
        print("Connecting to Antigravity Brain via PostgreSQL...")
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Applying Kwizz Monetization Schema...")
        # Note: This schema contains tables, policies, and functions.
        # RLS policies might conflict if they already exist, but this is a fresh application.
        cur.execute(sql)
        
        print("✅ Kwizz Monetization Schema applied successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")

if __name__ == "__main__":
    apply_kwizz_schema()
