
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

def test_full_sync():
    print("--- Kwizz 'God-Tier' Sync Verification ---")
    
    # 1. Get a quiz
    quizzes = supabase.from_("quizzes").select("*").limit(1).execute()
    quiz_id = quizzes.data[0]['id']
    print(f"Quiz: {quizzes.data[0]['title']}")

    # 2. Create Game
    pin = str(time.time())[-4:]
    game = supabase.from_("games").insert({
        "quiz_id": quiz_id,
        "pin": pin,
        "status": "lobby",
        "is_answer_revealed": False
    }).execute()
    game_id = game.data[0]['id']
    print(f"Game Created: {game_id}")

    # 3. Join a Player
    player = supabase.from_("players").insert({
        "game_id": game_id,
        "team_name": "Test Swarm"
    }).execute()
    player_id = player.data[0]['id']
    print(f"Player Joined: {player_id}")

    # 4. Start Game
    questions = supabase.from_("questions").select("*").eq("quiz_id", quiz_id).order("question_order").execute()
    first_q = questions.data[0]
    supabase.from_("games").update({
        "status": "active",
        "current_question_id": first_q['id'],
        "question_started_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }).eq("id", game_id).execute()
    print("Game Started!")

    # 5. TEST HARD-LOCK (Host Reveals Answer)
    print("\n[VERIFICATION] Setting is_answer_revealed = True...")
    supabase.from_("games").update({
        "is_answer_revealed": True
    }).eq("id", game_id).execute()
    
    # 6. Verify State
    v_game = supabase.from_("games").select("*").eq("id", game_id).execute()
    is_revealed = v_game.data[0]['is_answer_revealed']
    
    if is_revealed:
        print("SUCCESS: is_answer_revealed correctly set to True.")
    else:
        print("FAILURE: is_answer_revealed remains False.")

    # Cleanup
    supabase.from_("players").delete().eq("game_id", game_id).execute()
    supabase.from_("games").delete().eq("id", game_id).execute()
    print("\nTest Cleanup Complete.")

if __name__ == "__main__":
    test_full_sync()
