
import psycopg2
import os
from dotenv import load_dotenv

def verify_monetization_functions():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.env"
    load_dotenv(env_path)
    
    conn_string = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")
    if not conn_string:
        print("Missing ANTIGRAVITY_BRAIN_CONNECTION_STRING")
        return

    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        # Check for function existence
        print("Verifying Kwizz Monetization Functions...")
        
        cur.execute("""
            SELECT proname 
            FROM pg_proc 
            JOIN pg_namespace n ON n.oid = pronamespace 
            WHERE nspname = 'public' 
            AND proname IN ('check_host_access', 'deduct_credit');
        """)
        
        functions = cur.fetchall()
        found_names = [f[0] for f in functions]
        
        if 'check_host_access' in found_names:
            print("✅ check_host_access found.")
        else:
            print("❌ check_host_access NOT found.")
            
        if 'deduct_credit' in found_names:
            print("✅ deduct_credit found.")
        else:
            print("❌ deduct_credit NOT found.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify_monetization_functions()
