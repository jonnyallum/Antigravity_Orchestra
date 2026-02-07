
import psycopg2
import os
from dotenv import load_dotenv

def apply_betting_schema():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.env"
    load_dotenv(env_path)
    
    conn_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")
    if not conn_string:
        print("Missing ANTIGRAVITY_BRAIN_CONNECTION_STRING")
        return

    sql_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Ecosystems\Betting\betting_schema.sql"
    with open(sql_path, 'r') as f:
        sql = f.read()

    try:
        print("Connecting to Antigravity Brain via PostgreSQL...")
        # Use connection pooling or direct connection
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Applying Betting Hub Schema...")
        # Split by ';' to execute individually if needed, but standard SQL usually works
        cur.execute(sql)
        
        print("✅ Betting Hub Schema applied successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to apply schema: {e}")

if __name__ == "__main__":
    apply_betting_schema()
