"""Kwizz Supabase Diagnostic - checks tables, RLS, data, and game creation flow"""
import requests
import json

URL = "https://japkqygktnubcrmlttqt.supabase.co"
ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphcGtxeWdrdG51YmNybWx0dHF0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxNjE5NzgsImV4cCI6MjA4NTczNzk3OH0.WR8RawTd0un2XaKSC1n117M8OyvXzp1JQYy6RrbpiyE"
SERVICE = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphcGtxeWdrdG51YmNybWx0dHF0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDE2MTk3OCwiZXhwIjoyMDg1NzM3OTc4fQ.jE8j8FjQyqWkw8DtHHAjgYaNNKj_MjH5IUa2tUq2aUY"

anon_h = {"apikey": ANON, "Authorization": f"Bearer {ANON}"}
svc_h = {"apikey": SERVICE, "Authorization": f"Bearer {SERVICE}"}

def check(label, r):
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Status: {r.status_code}")
    print(f"  Content-Range: {r.headers.get('content-range', 'N/A')}")
    try:
        data = r.json()
        print(f"  Data: {json.dumps(data, indent=2)[:600]}")
    except:
        print(f"  Raw: {r.text[:400]}")
    return r

# 1. Quizzes via anon
print("\n🔍 KWIZZ SUPABASE DIAGNOSTIC")
print("=" * 60)

r = requests.get(f"{URL}/rest/v1/quizzes?select=id,title,category&limit=5", headers=anon_h)
check("1. QUIZZES (anon key - SELECT)", r)

# 2. Questions count via anon
r = requests.get(
    f"{URL}/rest/v1/questions?select=id&limit=1",
    headers={**anon_h, "Prefer": "count=exact"}
)
check("2. QUESTIONS (anon key - count)", r)

# 3. Games via anon (SELECT)
r = requests.get(f"{URL}/rest/v1/games?select=*&limit=5", headers=anon_h)
check("3. GAMES (anon key - SELECT)", r)

# 4. Try INSERT game via anon (this is what the app does)
# First get a quiz ID
r_quiz = requests.get(f"{URL}/rest/v1/quizzes?select=id&limit=1", headers=svc_h)
quiz_data = r_quiz.json()
quiz_id = quiz_data[0]["id"] if quiz_data else None
print(f"\n  Using quiz_id: {quiz_id}")

if quiz_id:
    r = requests.post(
        f"{URL}/rest/v1/games",
        headers={**anon_h, "Content-Type": "application/json", "Prefer": "return=representation"},
        json={"quiz_id": quiz_id, "pin": "8888", "status": "lobby"}
    )
    check("4. CREATE GAME (anon key - INSERT)", r)
    
    # Clean up test game
    if r.status_code in (200, 201):
        game_data = r.json()
        if game_data:
            game_id = game_data[0]["id"] if isinstance(game_data, list) else game_data["id"]
            requests.delete(
                f"{URL}/rest/v1/games?id=eq.{game_id}",
                headers=svc_h
            )
            print("  (cleaned up test game)")

# 5. Players via anon (SELECT)
r = requests.get(f"{URL}/rest/v1/players?select=*&limit=5", headers=anon_h)
check("5. PLAYERS (anon key - SELECT)", r)

# 6. Try INSERT player via anon
r = requests.post(
    f"{URL}/rest/v1/players",
    headers={**anon_h, "Content-Type": "application/json", "Prefer": "return=representation"},
    json={"game_id": "00000000-0000-0000-0000-000000000000", "team_name": "TestTeam"}
)
check("6. CREATE PLAYER (anon key - INSERT, expect FK error)", r)

# 7. Responses via anon
r = requests.get(f"{URL}/rest/v1/responses?select=*&limit=5", headers=anon_h)
check("7. RESPONSES (anon key - SELECT)", r)

# 8. Check via service key to see if RLS is the blocker
r = requests.get(f"{URL}/rest/v1/quizzes?select=id,title,category&limit=5", headers=svc_h)
check("8. QUIZZES (service key - bypass RLS)", r)

r = requests.get(f"{URL}/rest/v1/games?select=*&limit=5", headers=svc_h)
check("9. GAMES (service key - bypass RLS)", r)

print("\n\n✅ Diagnostic complete!")
