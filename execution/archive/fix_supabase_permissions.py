
import os
import psycopg2
from dotenv import load_dotenv

def fix_table_permissions():
    # Using the direct connection string provided by the user
    # Fallback to the pooler URL which resolved earlier
    db_url = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"
    
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # 1. Force schema cache reload (notify pgrst)
        cur.execute("NOTIFY pgrst, 'reload config';")
        
        # 2. Grant usage on schema public to anon
        cur.execute("GRANT USAGE ON SCHEMA public TO anon;")
        
        # 3. Grant select/insert on leads to anon
        cur.execute("GRANT ALL ON TABLE public.leads TO anon;")
        cur.execute("GRANT ALL ON TABLE public.leads TO service_role;")
        
        # 4. Ensure sequence permissions for serial ID
        cur.execute("GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon;")
        
        conn.commit()
        print("Permissions granted and Schema Cache reload triggered.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    fix_table_permissions()
