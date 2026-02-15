
import os
import json
import time
from dotenv import load_dotenv
from supabase import create_client, Client

# Load Env
ENV_PATH = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
load_dotenv(ENV_PATH)
URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(URL, KEY)

# This script is a stub for the agent to use the LLM to generate content.
# Since I am the agent, I will generate the content samples here.

NICHE_PACKS = [
    {
        "category": "Antigravity Agency Lore",
        "questions": [
            {"text": "Who is known as 'The Maestro' in the Antigravity Orchestra?", "answer": "Marcus Cole", "options": ["Jonny Allum", "Marcus Cole", "Sebastian Allum", "Priya Sharma"], "difficulty": "easy"},
            {"text": "Which agent is responsible for 'God-Tier' UI/UX design?", "answer": "Priya Sharma", "options": ["Patrick Nguyen", "Priya Sharma", "Rowan Blackthorn", "Sam Blackwood"], "difficulty": "easy"},
            {"text": "What is the name of the Antigravity OS version 4.0 architecture?", "answer": "The Hive Mind", "options": ["The Matrix", "The Hive Mind", "The Grid", "The Nexus"], "difficulty": "medium"}
        ]
    },
    {
        "category": "Space Exploration",
        "questions": [
            {"text": "Which planet is known as the 'Red Planet'?", "answer": "Mars", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "difficulty": "easy"},
            {"text": "What was the name of the first human-made object to reach the surface of the Moon?", "answer": "Luna 2", "options": ["Apollo 11", "Luna 2", "Sputnik 1", "Surveyor 1"], "difficulty": "hard"},
            {"text": "Which telescope was launched in 1990 and has provided some of the most detailed images of deep space?", "answer": "Hubble Space Telescope", "options": ["James Webb Telescope", "Hubble Space Telescope", "Spitzer Telescope", "Kepler Telescope"], "difficulty": "medium"}
        ]
    },
    {
        "category": "Retro Gaming Mythology",
        "questions": [
            {"text": "In which game did Mario first appear?", "answer": "Donkey Kong", "options": ["Super Mario Bros.", "Donkey Kong", "Mario Bros.", "Pac-Man"], "difficulty": "medium"},
            {"text": "What was the name of the first commercially successful video game?", "answer": "Pong", "options": ["Space Invaders", "Pong", "Asteroids", "Pac-Man"], "difficulty": "easy"},
            {"text": "Which company released the 'Game Boy' in 1989?", "answer": "Nintendo", "options": ["Sega", "Nintendo", "Sony", "Atari"], "difficulty": "easy"}
        ]
    }
]

def import_synthetic_questions(packs):
    total = 0
    for pack in packs:
        cat_name = pack['category']
        # Insert or Find Quiz
        quiz_res = supabase.table("quizzes").select("id").eq("title", f"{cat_name} - Elite Pack").execute()
        if quiz_res.data:
            quiz_id = quiz_res.data[0]['id']
        else:
            quiz_res = supabase.table("quizzes").insert({
                "title": f"{cat_name} - Elite Pack",
                "category": cat_name
            }).execute()
            quiz_id = quiz_res.data[0]['id']

        question_data = []
        for q in pack['questions']:
            question_data.append({
                "quiz_id": quiz_id,
                "text": q['text'],
                "type": "multiple_choice",
                "options": q['options'],
                "answer": q['answer'],
                "difficulty": q['difficulty']
            })
        
        res = supabase.table("questions").insert(question_data).execute()
        total += len(res.data)
    
    print(f"[SYNTHETIC] Imported {total} elite questions.")

if __name__ == "__main__":
    import_synthetic_questions(NICHE_PACKS)
