
import os
import requests
import json
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import Json
import html

from supabase import create_client, Client

def fetch_and_import_trivia(amount=50, category=None, difficulty=None):
    """Fetch questions from Open Trivia DB and import to Kwizz."""
    base_url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "type": "multiple"
    }
    if category: params["category"] = category
    if difficulty: params["difficulty"] = difficulty

    print(f"📡 Fetching {amount} questions from Open Trivia DB...")
    try:
        r = requests.get(base_url, params=params)
        data = r.json()
    except Exception as e:
        print(f"❌ Fetch failed: {e}")
        return

    if data['response_code'] != 0:
        print(f"❌ API Error: Response code {data['response_code']}")
        return

    questions = data['results']
    print(f"✅ Fetched {len(questions)} questions.")

    # Load Env
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\kwizz\.env.local"
    load_dotenv(env_path)
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    supabase: Client = create_client(url, key)

    try:
        # Group by category to create quizzes
        packs = {}
        for q in questions:
            cat = q['category']
            if cat not in packs:
                packs[cat] = []
            
            # Clean HTML entities
            text = html.unescape(q['question'])
            correct = html.unescape(q['correct_answer'])
            incorrect = [html.unescape(i) for i in q['incorrect_answers']]
            options = incorrect + [correct]
            import random
            random.shuffle(options)

            packs[cat].append({
                "text": text,
                "options": options,
                "answer": correct,
                "fact": f"Category: {cat}",
                "difficulty": q['difficulty'],
                "order": len(packs[cat]) + 1
            })

        import_count = 0
        for cat_name, q_list in packs.items():
            # 1. Insert Quiz
            quiz_res = supabase.table("quizzes").insert({
                "title": f"{cat_name} - AI Pack {int(time.time())}",
                "category": cat_name
            }).execute()
            
            quiz_id = quiz_res.data[0]['id']
            
            # 2. Insert Questions
            question_data = []
            for q in q_list:
                question_data.append({
                    "quiz_id": quiz_id,
                    "text": q['text'],
                    "type": "multiple_choice",
                    "options": q['options'],
                    "answer": q['answer'],
                    "fact": q['fact'],
                    "difficulty": q['difficulty'],
                    "question_order": q['order']
                })
            
            supabase.table("questions").insert(question_data).execute()
            import_count += len(q_list)
        
        print(f"🚀 Successfully imported {import_count} questions across {len(packs)} quizzes!")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")

if __name__ == "__main__":
    # Fetch in batches to get to hundreds
    for i in range(4): # 4 * 50 = 200
        print(f"\n--- Batch {i+1} ---")
        fetch_and_import_trivia(amount=50)
        print("⏳ Sleeping 5s for API limits...")
        time.sleep(5)
