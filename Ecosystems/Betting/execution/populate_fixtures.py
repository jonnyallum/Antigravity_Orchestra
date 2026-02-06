
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

def populate_fixtures():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\.env"
    load_dotenv(env_path)
    
    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    fixtures = [
        # Football - Saturday
        {"sport": "football", "event_name": "Manchester United vs Tottenham", "start_time": "2026-02-07T12:30:00Z", "venue": "Old Trafford"},
        {"sport": "football", "event_name": "Arsenal vs Sunderland", "start_time": "2026-02-07T15:00:00Z", "venue": "Emirates Stadium"},
        {"sport": "football", "event_name": "Wolverhampton Wanderers vs Chelsea", "start_time": "2026-02-07T15:00:00Z", "venue": "Molineux"},
        {"sport": "football", "event_name": "Newcastle vs Brentford", "start_time": "2026-02-07T17:30:00Z", "venue": "St. James' Park"},
        # Football - Sunday
        {"sport": "football", "event_name": "Liverpool vs Manchester City", "start_time": "2026-02-08T16:30:00Z", "venue": "Anfield"},
        {"sport": "football", "event_name": "Brighton vs Crystal Palace", "start_time": "2026-02-08T14:00:00Z", "venue": "Amex Stadium"},
        
        # Horse Racing - Saturday
        {"sport": "horse_racing", "event_name": "Kingmaker Novice Chase", "start_time": "2026-02-07T14:00:00Z", "venue": "Warwick"},
        {"sport": "horse_racing", "event_name": "Denman Chase", "start_time": "2026-02-07T14:30:00Z", "venue": "Newbury"},
        {"sport": "horse_racing", "event_name": "Game Spirit Chase", "start_time": "2026-02-07T15:15:00Z", "venue": "Newbury"},
    ]

    print(f"Syncing {len(fixtures)} fixtures to Antigravity Brain...")
    r = httpx.post(f"{url}/rest/v1/bet_fixtures", headers=headers, json=fixtures)
    if r.status_code in (200, 201):
        print("✅ Fixtures synced successfully!")
    else:
        print(f"❌ Failed to sync fixtures: {r.status_code} - {r.text}")

if __name__ == "__main__":
    populate_fixtures()
