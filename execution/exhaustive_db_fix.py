import psycopg2
import sys

def try_connect(host, port, user, dbname, password):
    try:
        print(f"Trying {user}@{host}:{port}/{dbname}...")
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            connect_timeout=5
        )
        print("  SUCCESS!")
        return conn
    except Exception as e:
        print(f"  FAILED: {e}")
        return None

def main():
    PROJECT_REF = "japkqygktnubcrmlttqt"
    PASSWORD = "Aprilia100!69."
    
    # Common Supabase host patterns
    hosts = [
        f"db.{PROJECT_REF}.supabase.co",
        f"aws-0-eu-west-2.pooler.supabase.com",
    ]
    
    # Common ports
    ports = [5432, 6543]
    
    # Common users
    users = [
        "postgres",
        f"postgres.{PROJECT_REF}",
        "authenticator"
    ]
    
    for host in hosts:
        for port in ports:
            for user in users:
                conn = try_connect(host, port, user, "postgres", PASSWORD)
                if conn:
                    # FOUND IT! Let's apply the fixes
                    conn.autocommit = True
                    cur = conn.cursor()
                    
                    print("\nApplying fixes...")
                    
                    # 1. Add column and unique constraint
                    try:
                        cur.execute("ALTER TABLE games ADD COLUMN IF NOT EXISTS question_started_at TIMESTAMPTZ;")
                        print("  Column 'question_started_at' ensured in 'games'.")
                        
                        # Add unique constraint to responses to prevent duplicate scoring
                        cur.execute("ALTER TABLE responses ADD CONSTRAINT unique_response_per_player_per_question UNIQUE (player_id, question_id);")
                        print("  Unique constraint added to 'responses'.")
                    except Exception as e:
                        if "already exists" in str(e).lower():
                            print("  Unique constraint already exists on 'responses'.")
                        else:
                            print(f"  Error adding column/constraint: {e}")
                    
                    # 2. Enable Realtime
                    tables = ["games", "players", "responses"]
                    for table in tables:
                        try:
                            # Use a DO block to avoid error if already member
                            cur.execute(f"ALTER PUBLICATION supabase_realtime ADD TABLE public.{table};")
                            print(f"  Added {table} to supabase_realtime.")
                        except Exception as e:
                            if "already member" in str(e).lower():
                                print(f"  {table} already in realtime publication.")
                            else:
                                print(f"  Error adding {table} to realtime: {e}")
                    
                    # 3. Check RLS
                    print("\nChecking RLS status...")
                    cur.execute("SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('games', 'players', 'responses', 'questions');")
                    for row in cur.fetchall():
                        print(f"    - {row[0]}: RLS {'ENABLED' if row[1] else 'DISABLED'}")
                        
                    cur.close()
                    conn.close()
                    print("\nMission Accomplished!")
                    return

if __name__ == "__main__":
    main()
