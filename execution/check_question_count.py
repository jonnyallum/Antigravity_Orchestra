
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load Env
ENV_PATH = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
load_dotenv(ENV_PATH)
URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(URL, KEY)

def check_count():
    res = supabase.table("questions").select("id", count="exact").execute()
    print(f"\n[STATUS] Current Question Count: {res.count}")
    
    res_quizzes = supabase.table("quizzes").select("id", count="exact").execute()
    print(f"[STATUS] Current Quiz Count: {res_quizzes.count}")

if __name__ == "__main__":
    check_count()
