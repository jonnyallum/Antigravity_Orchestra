
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv("ANTIGRAVITY_BRAIN_CONNECTION_STRING")

def populate_value_tasks():
    try:
        conn = psycopg2.connect(CONNECTION_STRING)
        cur = conn.cursor()
        
        tasks = [
            {
                "title": "SEO Trend Analysis",
                "desc": "Research emerging AI-search ranking factors and SGE (Search Generative Experience) updates.",
                "agent": "grace",
                "cron": "0 10 * * 1" # Weekly Monday
            },
            {
                "title": "Revenue Model Audit",
                "desc": "Analyze top 5 AI Venture Studios for new monetization structures and equity split models.",
                "agent": "felix",
                "cron": "0 11 * * 3" # Weekly Wednesday
            },
            {
                "title": "GitHub Alpha Discovery",
                "desc": "Scan GitHub for trending open-source AI frameworks or MCP servers that we can integrate.",
                "agent": "adrian",
                "cron": "0 8 * * *" # Daily
            },
            {
                "title": "Brand Voice Optimization",
                "desc": "Audit our public copy against the latest 'High-Conviction' brand guidelines.",
                "agent": "elena",
                "cron": "0 12 1 * *" # Monthly
            }
        ]
        
        print("Adding high-value recurring tasks...")
        for t in tasks:
            cur.execute("""
                INSERT INTO tasks (title, description, assigned_to, priority, status, is_recurring, cron_expression, next_run_at, created_by_ai)
                VALUES (%s, %s, %s, 'P2', 'pending', true, %s, NOW(), 'claude');
            """, (t['title'], t['desc'], t['agent'], t['cron']))
            
        conn.commit()
        cur.close()
        conn.close()
        print("Done. The Orchestra Heartbeat will now manage these cycles.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    populate_value_tasks()
