import os
import time
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env.local"
load_dotenv(env_path)

supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Use Service Role for simulation

if not supabase_url or not supabase_key:
    print("Error: Missing credentials in .env.local")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

def simulate_monetized_flow():
    print("--- Starting Monetized Flow Simulation ---")
    
    # 1. Create a trial host
    email = f"tester_{int(time.time())}@kwizz.co.uk"
    print(f"Creating host with email: {email}")
    host_res = supabase.from_("hosts").insert({
        "email": email,
        "display_name": "Simulation Host"
    }).execute()
    
    if not host_res.data:
        print("Failed to create host")
        return
    
    host_id = host_res.data[0]['id']
    credits = host_res.data[0]['free_credits_remaining']
    print(f"Host Created! ID: {host_id} | Credits: {credits}")

    # 2. Get a quiz
    quiz_res = supabase.from_("quizzes").select("*").limit(1).execute()
    quiz_id = quiz_res.data[0]['id']
    print(f"Using Quiz ID: {quiz_id}")

    # 3. Simulate 3 successful game creations
    for i in range(1, 4):
        print(f"\nAttempting Game Creation #{i}...")
        
        # Check credits (logic matches useGameSync.ts)
        host_data = supabase.from_("hosts").select("free_credits_remaining").eq("id", host_id).single().execute()
        current_credits = host_data.data['free_credits_remaining']
        
        if current_credits > 0:
            # Create Game
            pin = str(time.time())[-4:]
            game = supabase.from_("games").insert({
                "quiz_id": quiz_id,
                "pin": pin,
                "status": "lobby",
                "host_id": host_id
            }).execute()
            
            if game.data:
                print(f"  SUCCESS: Game created with PIN {pin}")
                # Deduct
                supabase.from_("hosts").update({"free_credits_remaining": current_credits - 1}).eq("id", host_id).execute()
                print(f"  Credit Deducted. Remaining: {current_credits - 1}")
            else:
                print("  FAILED to create game")
        else:
            print("  FAILED: Out of credits")

    # 4. Attempt 4th game (should fail credits check)
    print("\nAttempting Game Creation #4 (should fail)...")
    host_data = supabase.from_("hosts").select("free_credits_remaining").eq("id", host_id).single().execute()
    current_credits = host_data.data['free_credits_remaining']
    
    if current_credits <= 0:
        print("  CORRECT: Request blocked due to insufficient credits (0).")
    else:
        print(f"  WRONG: Host still has {current_credits} credits. Logic failure.")

    print("\n--- Monetization Simulation Complete ---")

if __name__ == "__main__":
    simulate_monetized_flow()
