
import requests
import uuid

API_URL = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/rpc/submit_lead"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    # Simulate Browser Headers
    "Origin": "https://insydetradar.com",
    "Referer": "https://insydetradar.com/"
}

# Generate random email to avoid 409
random_email = f"debug_{uuid.uuid4().hex[:8]}@test.com"
payload = {"email_input": random_email}

print(f"Testing RPC with email: {random_email}")
try:
    r = requests.post(API_URL, headers=headers, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
    print("Response Headers:", r.headers)
except Exception as e:
    print(f"Error: {e}")
