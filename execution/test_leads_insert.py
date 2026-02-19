
import requests
import json
import os

def test_anon_insert():
    url = "https://kerqqobkiziadwtkpprx.supabase.co/rest/v1/leads"
    anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlcnFxb2JraXppYWR3dGtwcHJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk4OTg2MzUsImV4cCI6MjA4NTQ3NDYzNX0.9g0ddCqS2ZlCa7HlEhKlJxYumx-VKK7dyPkQCHXrVio"
    
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    data = {
        "email": "agent_test_autobot@insydetradar.com",
        "user_agent": "Antigravity/AgOS-Python-Test-Agent"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("SUCCESS: Lead inserted via Anon Key.")
            print("Response:", response.json())
        else:
            print(f"FAILED: Status {response.status_code}")
            print("Response:", response.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_anon_insert()
