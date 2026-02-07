import os
import requests
from dotenv import load_dotenv

def get_brain_agents():
    load_dotenv()
    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_ANON_KEY")
    
    if not url or not key:
        print("Missing URL or Key")
        return

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }
    
    try:
        response = requests.get(f"{url}/rest/v1/agents?select=*", headers=headers)
        if response.status_code == 200:
            agents = response.json()
            print(f"Found {len(agents)} agents in Shared Brain:")
            for a in agents:
                print(f"- {a.get('handle', a.get('agent_id'))} | {a.get('nickname')} | {a.get('role')}")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    get_brain_agents()
