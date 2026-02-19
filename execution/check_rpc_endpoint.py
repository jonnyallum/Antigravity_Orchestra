
import requests

# API URL for RPC
# We are calling the function 'api.submit_lead' which we created in the 'api' schema
# PostgREST exposes schema-bound functions differently.
# Standard: /rpc/function_name
# But we need to check if 'api' schema is in the search path of the configuration.
# If the exposed schema is 'public,storage,api', then /rpc/submit_lead might work.
# If not, we might fail to find it.

API_URL = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/rpc/submit_lead"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json"
}

payload = {"email_input": "debug_schema_test@test.com"}

print("Testing RPC visibility...")
try:
    r = requests.post(API_URL, headers=headers, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
