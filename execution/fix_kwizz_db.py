import psycopg2
import os
from dotenv import load_dotenv

def check_and_fix_db():
    PROJECT_REF = "japkqygktnubcrmlttqt"
    print(f"Checking database for Kwizz ({PROJECT_REF})...")
    
    try:
        conn = psycopg2.connect(
            host=f"aws-0-eu-west-2.pooler.supabase.com",
            port=6543,
            dbname="postgres",
            user=f"postgres.{PROJECT_REF}",
            password="Aprilia100!69.",
            connect_timeout=10
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1. Check for question_started_at column
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'games' AND column_name = 'question_started_at';
        """)
        if cur.fetchone():
            print("  Column 'question_started_at' already exists in 'games' table.")
        else:
            print("  Column 'question_started_at' missing. Adding it...")
            cur.execute("ALTER TABLE games ADD COLUMN question_started_at TIMESTAMPTZ;")
            print("  Added 'question_started_at' to 'games'.")
            
        # 2. Enable Realtime
        tables = ['games', 'players', 'responses']
        for table in tables:
            try:
                cur.execute(f"ALTER PUBLICATION supabase_realtime ADD TABLE public.{table};")
                print(f"  Added {table} to supabase_realtime")
            except Exception as e:
                err_str = str(e).lower()
                if 'already member' in err_str:
                    print(f"  {table} is already a member of supabase_realtime.")
                else:
                    print(f"  Error adding {table} to realtime: {e}")
                    
        # 3. Check RLS (Simplified check)
        print("  Verifying RLS policies (manual review recommended)...")
        cur.execute("SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('games', 'players', 'responses', 'questions');")
        for row in cur.fetchall():
            print(f"    - {row[0]}: RLS {'ENABLED' if row[1] else 'DISABLED'}")
            
        cur.close()
        conn.close()
        print("\nDatabase maintenance complete!")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    check_and_fix_db()
