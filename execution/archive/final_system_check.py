
import requests

def check_systems():
    # 1. Auth Check - Supabase URL
    # We check the project URL used in the app, not the custom domain yet, as script.js uses the project URL.
    auth_url = "https://kerqqobkiziadwtkpprx.supabase.co/auth/v1/authorize?provider=google&redirect_to=https://insydetradar.com"
    print(f"Checking Auth URL: {auth_url}")
    try:
        # allow_redirects=False to see the 303 to Google
        r = requests.get(auth_url, allow_redirects=False)
        print(f"Auth Status: {r.status_code}")
        if r.status_code in [302, 303]:
            loc = r.headers.get('Location', '')
            if 'accounts.google.com' in loc:
                print("✅ Auth Config: SUCCESS (Redirects to Google)")
            else:
                print(f"⚠️ Auth Config: REDIRECTS to {loc}")
        elif r.status_code == 200:
             print("ℹ️ Auth Config: Returned 200 (Might be a direct page?)")
        else:
             print(f"❌ Auth Config: FAILED ({r.text})")
    except Exception as e:
        print(f"❌ Auth Config: Error {e}")

    # 2. API Check
    api_url = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/leads"
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    payload = {"email": "system_check_auth_complete@insydetradar.com"}
    
    print(f"\nChecking API URL: {api_url}")
    try:
        r = requests.post(api_url, headers=headers, json=payload)
        if r.status_code in [200, 201]:
            print("✅ API Cache: SUCCESS (Lead inserted)")
        elif r.status_code == 404:
            print("❌ API Cache: FAILED (404 - Table not found in cache)")
        else:
             print(f"❌ API Cache: FAILED ({r.status_code} - {r.text})")
    except Exception as e:
        print(f"❌ API Cache: Error {e}")

if __name__ == "__main__":
    check_systems()
