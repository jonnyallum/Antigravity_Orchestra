
import requests
import os
from dotenv import load_dotenv

def get_count():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env.local"
    load_dotenv(env_path)
    url = f"{os.getenv('NEXT_PUBLIC_SUPABASE_URL')}/rest/v1/quizzes?select=count"
    headers = {
        'apikey': os.getenv('SUPABASE_SERVICE_ROLE_KEY'),
        'Authorization': f"Bearer {os.getenv('SUPABASE_SERVICE_ROLE_KEY')}"
    }
    r = requests.get(url, headers=headers)
    print(f"Total Quizzes: {r.json()[0]['count']}")

if __name__ == "__main__":
    get_count()
