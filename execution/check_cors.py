
import requests

API_URL = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/leads"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Origin": "https://insydetradar.com",  # MIMIC BROWSER
    "Access-Control-Request-Method": "POST"
}

print("Testing CORS OPTIONS...")
try:
    r = requests.options(API_URL, headers=headers)
    print(f"Status: {r.status_code}")
    print("Headers:", r.headers)
    
    if 'Access-Control-Allow-Origin' in r.headers:
        print(f"✅ CORS Allowed: {r.headers['Access-Control-Allow-Origin']}")
    else:
        print("❌ CORS Missing Allow-Origin Header")
except Exception as e:
    print(f"Error: {e}")
