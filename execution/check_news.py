
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def check_heartbeat_activity():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        # Check for new system news in the last 30 minutes
        cur.execute("SELECT title, content, created_at FROM system_news WHERE created_at > NOW() - INTERVAL '30 minutes' ORDER BY created_at DESC")
        news = cur.fetchall()
        
        if news:
            print("\n--- Recent Heartbeat Activity ---")
            for title, content, created_at in news:
                print(f"[{created_at}] {title}: {content}")
        else:
            print("\nNo autonomous activity detected in the last 30 minutes.")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_heartbeat_activity()
