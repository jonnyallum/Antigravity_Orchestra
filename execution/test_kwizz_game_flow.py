"""Test the exact game flow: create game, update status, set question"""
import requests
import json

URL = "https://japkqygktnubcrmlttqt.supabase.co"
ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphcGtxeWdrdG51YmNybWx0dHF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxNjE5NzgsImV4cCI6MjA4NTczNzk3OH0.WR8RawTd0un2XaKSC1n117M8OyvXzp1JQYy6RrbpiyE"
SERVICE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphcGtxeWdrdG51YmNybWx0dHF0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDE2MTk3OCwiZXhwIjoyMDg1NzM3OTc4fQ.jE8j8FjQyqWkw8DtHHAjgYaNNKj_MjH5IUa2tUq2aUY"

anon_h = {"apikey": ANON, "Authorization": f"Bearer {ANON}", "Content-Type": "application/json", "Prefer": "return=representation"}
svc_h = {"apikey": SERVICE, "Authorization": f"Bearer {SERVICE}", "Content-Type": "application/json", "Prefer": "return=representation"}

# Step 1: Get a quiz and its first question
print("=== STEP 1: Get quiz + question ===")
r = requests.get(f"{URL}/rest/v1/quizzes?select=id&limit=1", headers=svc_h)
quiz_id = r.json()[0]["id"]
print(f"Quiz ID: {quiz_id}")

r = requests.get(f"{URL}/rest/v1/questions?select=id&quiz_id=eq.{quiz_id}&order=question_order&limit=1", headers=svc_h)
question_id = r.json()[0]["id"]
print(f"First Question ID: {question_id}")

# Step 2: Create a game (anon key - like the app does)
print("\n=== STEP 2: Create game (anon key) ===")
r = requests.post(f"{URL}/rest/v1/games", headers=anon_h, json={"quiz_id": quiz_id, "pin": "7777", "status": "lobby"})
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")
if r.status_code not in (200, 201):
    print("FAILED to create game!")
    exit()
game = r.json()[0] if isinstance(r.json(), list) else r.json()
game_id = game["id"]
print(f"Game ID: {game_id}")

# Step 3: UPDATE game status to 'active' (anon key - THIS IS WHAT FAILS)
print("\n=== STEP 3: UPDATE game status to 'active' (anon key) ===")
r = requests.patch(
    f"{URL}/rest/v1/games?id=eq.{game_id}",
    headers=anon_h,
    json={"status": "active"}
)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")

# Step 4: UPDATE current_question_id (anon key)
print("\n=== STEP 4: SET current_question_id (anon key) ===")
r = requests.patch(
    f"{URL}/rest/v1/games?id=eq.{game_id}",
    headers=anon_h,
    json={"current_question_id": question_id}
)
print(f"Status: {r.status_code}")
print(f"Response: {r.text[:300]}")

# Step 5: Verify the game state
print("\n=== STEP 5: Verify game state ===")
r = requests.get(f"{URL}/rest/v1/games?id=eq.{game_id}&select=*", headers=svc_h)
print(f"Status: {r.status_code}")
game_state = r.json()
print(f"Game state: {json.dumps(game_state, indent=2)[:400]}")

# Cleanup
print("\n=== CLEANUP ===")
r = requests.delete(f"{URL}/rest/v1/games?id=eq.{game_id}", headers=svc_h)
print(f"Deleted test game: {r.status_code}")
