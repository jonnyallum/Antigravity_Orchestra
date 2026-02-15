
import os
import requests
import json
import time
import hashlib
from dotenv import load_dotenv
import html
from supabase import create_client, Client

# Load Env
ENV_PATH = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
load_dotenv(ENV_PATH)
URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(URL, KEY)

def get_question_hash(text):
    return hashlib.md5(text.strip().lower().encode()).hexdigest()

def fetch_from_opentdb(amount=50):
    url = "https://opentdb.com/api.php"
    params = {"amount": amount, "type": "multiple"}
    r = requests.get(url, params=params)
    data = r.json()
    if data['response_code'] != 0: return []
    
    results = []
    for q in data['results']:
        correct = html.unescape(q['correct_answer'])
        incorrect = [html.unescape(i) for i in q['incorrect_answers']]
        options = incorrect + [correct]
        import random
        random.shuffle(options)
        results.append({
            "text": html.unescape(q['question']),
            "answer": correct,
            "options": options,
            "category": q['category'],
            "difficulty": q['difficulty'],
            "source": "OpenTDB"
        })
    return results

def fetch_from_jservice(amount=50):
    try:
        # jService returns random questions
        url = f"http://jservice.io/api/random?count={amount}"
        r = requests.get(url, timeout=10)
        data = r.json()
        
        results = []
        for q in data:
            if not q['question'] or not q['answer']: continue
            results.append({
                "text": q['question'],
                "answer": q['answer'],
                "options": None,
                "category": q['category']['title'] if q['category'] else "General",
                "difficulty": "medium",
                "source": "jService"
            })
        return results
    except Exception as e:
        print(f"[ERROR] jService Fetch failed: {e}")
        return []

def import_questions(questions):
    if not questions: return
    
    # 1. Deduplication: Fetch existing hashes (or use unique constraint in DB)
    # For now, we'll just try to insert and let the DB handle it if we add a constraint,
    # or we filter here against a quick check.
    
    packs = {}
    for q in questions:
        cat = q['category']
        if cat not in packs: packs[cat] = []
        packs[cat].append(q)

    total_imported = 0
    for cat_name, q_list in packs.items():
        # Insert or Find Quiz
        quiz_res = supabase.table("quizzes").select("id").eq("title", f"{cat_name} - Master Pack").execute()
        if quiz_res.data:
            quiz_id = quiz_res.data[0]['id']
        else:
            quiz_res = supabase.table("quizzes").insert({
                "title": f"{cat_name} - Master Pack",
                "category": cat_name
            }).execute()
            quiz_id = quiz_res.data[0]['id']

        question_data = []
        for q in q_list:
            q_type = "multiple_choice"
            options = q['options']
            answer = q['answer']
            
            if not options:
                # Open-ended questions are usually Numeral or Letters
                if answer.replace('.', '', 1).isdigit():
                    q_type = "numeral"
                else:
                    q_type = "letters"
            
            question_data.append({
                "quiz_id": quiz_id,
                "text": q['text'],
                "type": q_type,
                "options": options,
                "answer": answer,
                "difficulty": q['difficulty']
            })
        
        try:
            # Using 'on_conflict' if we had a unique constraint, otherwise just insert
            res = supabase.table("questions").insert(question_data).execute()
            total_imported += len(res.data)
        except Exception as e:
            print(f"Skipping batch due to collision or error: {e}")

    print(f"[SWARM] Imported {total_imported} new questions.")

def fetch_from_the_trivia_api(amount=50):
    url = "https://the-trivia-api.com/v2/questions"
    params = {"limit": amount}
    r = requests.get(url, params=params)
    data = r.json()
    
    results = []
    for q in data:
        correct = q['correctAnswer']
        incorrect = q['incorrectAnswers']
        options = incorrect + [correct]
        import random
        random.shuffle(options)
        results.append({
            "text": q['question']['text'],
            "answer": correct,
            "options": options,
            "category": q['category'],
            "difficulty": q['difficulty'],
            "source": "TheTriviaAPI"
        })
    return results

if __name__ == "__main__":
    sources = [fetch_from_opentdb, fetch_from_jservice, fetch_from_the_trivia_api]
    for i in range(40): # Final Push: 40 * 150 = 6000 target questions (+4800 existing)
        print(f"\n[LAUNCH] --- GLOBAL SWARM PHASE 4 FINAL PUSH {i+1}/40 ---")
        for source_fn in sources:
            print(f"\n--- Swarming from {source_fn.__name__} ---")
            qs = source_fn(50)
            import_questions(qs)
            time.sleep(3)
