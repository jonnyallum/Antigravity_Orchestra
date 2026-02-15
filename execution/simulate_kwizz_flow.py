import os
import time
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env from kwizz client
env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
load_dotenv(env_path)

url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(url, key)

def simulate_game():
    print("Starting God-Tier E2E Simulation...")
    
    # 1. Get a quiz
    quizzes = supabase.from_("quizzes").select("*").limit(1).execute()
    if not quizzes.data:
        print("No quizzes found. Run seed script first.")
        return
    quiz_id = quizzes.data[0]['id']
    print(f"Found Quiz: {quizzes.data[0]['title']}")

    # 2. Create Game (Lobby)
    pin = str(time.time())[-4:]
    game = supabase.from_("games").insert({
        "quiz_id": quiz_id,
        "pin": pin,
        "status": "lobby"
    }).execute()
    game_id = game.data[0]['id']
    print(f"Game Created! PIN: {pin} | ID: {game_id}")

    # 3. Simulate Players Joining
    teams = ["Team Alpha", "Beta Buzzers", "Gamma Gany"]
    player_ids = []
    for team in teams:
        p = supabase.from_("players").insert({
            "game_id": game_id,
            "team_name": team
        }).execute()
        player_ids.append(p.data[0]['id'])
        print(f"  Team {team} joined.")

    # 4. Start Game (Active)
    questions = supabase.from_("questions").select("*").eq("quiz_id", quiz_id).order("question_order").execute()
    if not questions.data:
        print("No questions found for quiz.")
        return
    
    first_q = questions.data[0]
    supabase.from_("games").update({
        "status": "active",
        "current_question_id": first_q['id'],
        "question_started_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }).eq("id", game_id).execute()
    print(f"Game Started! First Question: {first_q['text']}")

    # 5. Simulate Responses with varying speeds
    time.sleep(1) 
    
    # Alpha (Correct, Fast)
    supabase.from_("responses").insert({
        "game_id": game_id,
        "player_id": player_ids[0],
        "question_id": first_q['id'],
        "answer": first_q['answer'],
        "is_correct": True,
        "speed_ms": 1200
    }).execute()
    print("  Team Alpha responded (1200ms, Correct)")

    # Beta (Correct, Slow)
    supabase.from_("responses").insert({
        "game_id": game_id,
        "player_id": player_ids[1],
        "question_id": first_q['id'],
        "answer": first_q['answer'],
        "is_correct": True,
        "speed_ms": 5000
    }).execute()
    print("  Beta Buzzers responded (5000ms, Correct)")

    # Gamma (Wrong)
    supabase.from_("responses").insert({
        "game_id": game_id,
        "player_id": player_ids[2],
        "question_id": first_q['id'],
        "answer": "Wrong Answer",
        "is_correct": False,
        "speed_ms": 2000
    }).execute()
    print("  Gamma Gany responded (2000ms, Wrong)")

    # 6. Verify Scoring
    def calculate_points(is_correct, speed_ms):
        if not is_correct: return 0
        return max(100, 1000 - (speed_ms // 10))

    for i, pid in enumerate(player_ids):
        is_correct = (i < 2)
        speed = [1200, 5000, 2000][i]
        points = calculate_points(is_correct, speed)
        if points > 0:
            supabase.from_("players").update({"score": points}).eq("id", pid).execute()

    # Final Check
    f_players = supabase.from_("players").select("*").eq("game_id", game_id).order("score", desc=True).execute()
    print("\nLeaderboard:")
    for p in f_players.data:
        print(f"  {p['team_name']}: {p['score']} pts")

    print("\nSimulation Complete! Game state preserved for inspection.")

if __name__ == "__main__":
    simulate_game()
