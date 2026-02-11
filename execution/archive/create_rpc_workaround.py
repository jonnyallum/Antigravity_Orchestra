
import psycopg2
import requests
import json

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

# 1. Create RPC Function
sql = """
CREATE OR REPLACE FUNCTION public.submit_lead(email_input text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  INSERT INTO public.leads (email) VALUES (email_input);
  RETURN json_build_object('status', 'ok', 'email', email_input);
END;
$$;

GRANT EXECUTE ON FUNCTION public.submit_lead(text) TO anon, authenticated, service_role;
NOTIFY pgrst, 'reload config';
"""

print("--- 1. CREATING RPC FUNCTION ---")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("SUCCESS: Function public.submit_lead created and permissions granted.")
    conn.close()
except Exception as e:
    print(f"SQL ERROR: {e}")
    exit(1)

# 2. Test RPC via API
print("\n--- 2. TESTING RPC VIA API ---")
API_URL = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/rpc/submit_lead"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json"
}

payload = {"email_input": "rpc_test_v1@insydetradar.com"}

try:
    r = requests.post(API_URL, headers=headers, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
    
    if r.status_code == 200:
        print("✅ RPC SUCCESS! We can bypass the table cache.")
    else:
        print("❌ RPC FAILED.")
except Exception as e:
    print(f"API ERROR: {e}")
