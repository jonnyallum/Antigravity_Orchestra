
import os
import psycopg2
from dotenv import load_dotenv

def check_supabase_connection():
    # Load from the Insydetradar specific .env
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\Insydetradar\Insydetradar\.env"
    load_dotenv(env_path)
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        print(f"Connecting to Supabase PostgreSQL...")
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # Check if users table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');")
        exists = cur.fetchone()[0]
        print(f"Table 'users' exists: {exists}")
        
        if not exists:
            print("Table 'users' does not exist. The database might be empty.")
        else:
            cur.execute("SELECT count(*) FROM users;")
            count = cur.fetchone()[0]
            print(f"Total users in DB: {count}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    check_supabase_connection()
