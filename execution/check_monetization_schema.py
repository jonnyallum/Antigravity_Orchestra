import os
import psycopg2
from dotenv import load_dotenv

# Load env from kwizz client
env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env.local"
load_dotenv(env_path)

# Database connection details
PROJECT_REF = "japkqygktnubcrmlttqt"
db_host = f"db.{PROJECT_REF}.supabase.co"
password = "Aprilia100!69."

def check_schema():
    conn_str = f"host={db_host} port=5432 user=postgres dbname=postgres password={password} sslmode=require"
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        tables = ["hosts", "host_credits", "host_subscriptions", "player_prime", "sponsor_rounds"]
        
        for table in tables:
            print(f"\n--- Table: {table} ---")
            try:
                cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position;")
                cols = cur.fetchall()
                if not cols:
                    print(f"Table '{table}' does not exist.")
                else:
                    for col in cols:
                        print(f"  {col[0]}: {col[1]}")
            except Exception as e:
                print(f"Error checking {table}: {e}")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_schema()
