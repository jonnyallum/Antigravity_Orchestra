
import httpx
import os
from dotenv import load_dotenv

def setup_betting_schema():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\.env"
    load_dotenv(env_path)
    
    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY")
    
    if not url or not key:
        print("Missing Antigravity Brain credentials")
        return

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    # We can't easily CREATE tables via REST API in Supabase (need SQL Editor)
    # But we can check if they exist.
    tables = ["bet_fixtures", "bet_predictions", "bet_results", "bet_performance"]
    
    print(f"Checking Betting Hub Schema on {url}...")
    
    for table in tables:
        r = httpx.get(f"{url}/rest/v1/{table}?select=count", headers=headers)
        if r.status_code == 200:
            print(f"✅ Table '{table}' exists.")
        else:
            print(f"❌ Table '{table}' not found (Status: {r.status_code})")

if __name__ == "__main__":
    setup_betting_schema()
