
import os
import psycopg2
import requests
import json

# Configuration
DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"
API_URL = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/leads"

# Keys
SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2OTg5ODYzNSwiZXhwIjoyMDg1NDc0NjM1fQ.ZKCRj0m1deLpNy_0gPYgOLRrcMamloQBCot99Nvw71g"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"

def run_diagnostics():
    print("--- 1. SCHEMA REFRESH (SQL) ---")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("NOTIFY pgrst, 'reload config';")
        conn.commit()
        print("SUCCESS: 'NOTIFY pgrst, reload config' sent.")
        conn.close()
    except Exception as e:
        print(f"ERROR: SQL Connection failed: {e}")

    print("\n--- 2. SERVICE ROLE INSERT (ADMIN) ---")
    headers_service = {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload_service = {"email": "agent_admin_verify@insydetradar.com", "user_agent": "AgOS-Admin-Verify"}
    
    try:
        resp = requests.post(API_URL, headers=headers_service, json=payload_service)
        if resp.status_code in [200, 201]:
            print(f"SUCCESS: Inserted via Service Key. ID: {resp.json()[0]['id']}")
        else:
            print(f"FAILED: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"ERROR: Request failed: {e}")

    print("\n--- 3. ANON KEY INSERT (PUBLIC) ---")
    headers_anon = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload_anon = {"email": "agent_public_verify@insydetradar.com", "user_agent": "AgOS-Public-Verify"}
    
    try:
        resp = requests.post(API_URL, headers=headers_anon, json=payload_anon)
        if resp.status_code in [200, 201]:
            print(f"SUCCESS: Inserted via Anon Key. ID: {resp.json()[0]['id']}")
        else:
            print(f"FAILED: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"ERROR: Request failed: {e}")

if __name__ == "__main__":
    run_diagnostics()
