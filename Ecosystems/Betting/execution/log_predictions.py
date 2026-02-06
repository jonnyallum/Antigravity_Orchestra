
import httpx
import os
from dotenv import load_dotenv
import random

def generate_predictions():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\.env"
    load_dotenv(env_path)
    
    url = os.getenv("ANTIGRAVITY_BRAIN_URL")
    key = os.getenv("ANTIGRAVITY_BRAIN_SERVICE_ROLE_KEY")
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    # Fetch fixture IDs to link to
    r = httpx.get(f"{url}/rest/v1/bet_fixtures?select=id,event_name", headers=headers)
    fixtures = {f['event_name']: f['id'] for f in r.json()}
    
    predictions = []

    # --- 1. FOOTBALL ACCUMULATORS (20) ---
    # We'll generate permutations of the Saturday fixtures
    sat_fixtures = ["Manchester United vs Tottenham", "Arsenal vs Sunderland", "Wolverhampton Wanderers vs Chelsea", "Newcastle vs Brentford"]
    for i in range(20):
        # Sample random 3-folds
        selection = random.sample(sat_fixtures, 3)
        acc_data = {
            "title": f"Saturday High-Velocity Acca #{i+1}",
            "legs": [{"match": m, "pick": "Home Win" if "United" in m or "Arsenal" in m else "Over 2.5 Goals"} for m in selection],
            "odds": round(random.uniform(5.0, 15.0), 2)
        }
        predictions.append({
            "fixture_id": fixtures.get("Manchester United vs Tottenham"), # Linking to primary fixture
            "prediction_type": "accumulator",
            "prediction_data": acc_data,
            "conviction_score": round(random.uniform(0.6, 0.9), 2),
            "algorithm_version": "Gaffer_v3.0"
        })

    # --- 2. ANYTIME GOALSCORERS (20) ---
    scorers = ["Marcus Rashford", "Son Heung-min", "Bukayo Saka", "Cole Palmer", "Alexander Isak", "Erling Haaland", "Mohamed Salah"]
    for i in range(20):
        scorer = random.choice(scorers)
        match = "Manchester United vs Tottenham" if scorer in ["Rashford", "Son"] else "Liverpool vs Manchester City"
        predictions.append({
            "fixture_id": fixtures.get(match),
            "prediction_type": "goalscorer",
            "prediction_data": {"player": scorer, "market": "Anytime Goalscorer", "odds": 2.25},
            "conviction_score": 0.85,
            "algorithm_version": "Gaffer_v3.0"
        })

    # --- 3. HORSE RACING (Kingmaker Tricast) ---
    # Runners: Steel Ally (4/6), Mambonumberfive (6/4), Mirabad (15/2), Hansard, Meetmebythesea, Lulamba
    tricasts = [
        {"1st": "Steel Ally", "2nd": "Mambonumberfive", "3rd": "Mirabad"},
        {"1st": "Mambonumberfive", "2nd": "Steel Ally", "3rd": "Hansard"},
        {"1st": "Steel Ally", "2nd": "Mirabad", "3rd": "Meetmebythesea"}
    ]
    for tc in tricasts:
        predictions.append({
            "fixture_id": fixtures.get("Kingmaker Novice Chase"),
            "prediction_type": "tricast",
            "prediction_data": tc,
            "conviction_score": 0.72,
            "algorithm_version": "Handicapper_v3.0"
        })

    # --- 4. WIN SELECTIONS (Horses) ---
    wins = [
        {"horse": "Steel Ally", "race": "Kingmaker Novice Chase"},
        {"horse": "Protektorat", "race": "Denman Chase"}, # Note: Checking expected runners for other races
        {"horse": "Edwardstone", "race": "Game Spirit Chase"}
    ]
    for w in wins:
        predictions.append({
            "fixture_id": fixtures.get(w['race']),
            "prediction_type": "win",
            "prediction_data": w,
            "conviction_score": 0.90,
            "algorithm_version": "Handicapper_v3.0"
        })

    print(f"Uploading {len(predictions)} predictions to Supabase...")
    r = httpx.post(f"{url}/rest/v1/bet_predictions", headers=headers, json=predictions)
    if r.status_code in (200, 201):
        print("✅ Predictions successfully logged!")
    else:
        print(f"❌ Upload failed: {r.status_code} - {r.text}")

if __name__ == "__main__":
    generate_predictions()
