
import httpx
import os
from dotenv import load_dotenv

def generate_bet_report():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\.env"
    load_dotenv(env_path)
    
    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}"
    }

    try:
        r = httpx.get(f"{url}/rest/v1/bet_predictions?select=*", headers=headers)
        predictions = r.json()
        
        r_fix = httpx.get(f"{url}/rest/v1/bet_fixtures?select=id,event_name", headers=headers)
        fixtures_map = {f['id']: f['event_name'] for f in r_fix.json()}

        lines = ["# 🎰 Current Active Bets (Next 48 Hours)", "> Pending Results", ""]
        
        for p in predictions:
            event = fixtures_map.get(p['fixture_id'], "Unknown")
            p_type = p['prediction_type']
            data = p['prediction_data']
            lines.append(f"- **{event}** [{p_type}]: {data}")

        target_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Ecosystems\Betting\docs\LATEST_BETS.md"
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print("Done")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_bet_report()
