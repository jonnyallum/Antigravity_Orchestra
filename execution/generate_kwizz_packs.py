
import os
import json
from dotenv import load_dotenv
import httpx

QUIZ_PACKS = [
    {
        "title": "F1: The Turbo Era",
        "category": "Sports",
        "questions": [
            {"text": "Which driver has the most F1 World Championships?", "options": ["Lewis Hamilton", "Michael Schumacher", "Ayrton Senna", "Both Hamilton & Schumacher"], "answer": "Both Hamilton & Schumacher", "fact": "They both hold 7 world titles.", "difficulty": "easy", "order": 1},
            {"text": "What does DRS stand for in F1?", "options": ["Drag Reduction System", "Direct Racing Speed", "Downforce Regulation Sector", "Drive Recovery Soft"], "answer": "Drag Reduction System", "fact": "DRS was introduced in 2011 to aid overtaking.", "difficulty": "medium", "order": 2},
            {"text": "Which track is known as the 'Temple of Speed'?", "options": ["Monza", "Silverstone", "Spa", "Suzuka"], "answer": "Monza", "fact": "Monza features some of the highest average speeds in the F1 calendar.", "difficulty": "medium", "order": 3},
            {"text": "Who won the first ever F1 World Championship in 1950?", "options": ["Juan Manuel Fangio", "Giuseppe Farina", "Alberto Ascari", "Stirling Moss"], "answer": "Giuseppe Farina", "fact": "Farina won in an Alfa Romeo.", "difficulty": "hard", "order": 4},
            {"text": "Which team has the most Constructors' Championships?", "options": ["Ferrari", "McLaren", "Williams", "Mercedes"], "answer": "Ferrari", "fact": "Ferrari has 16 titles.", "difficulty": "medium", "order": 5}
        ]
    },
    {
        "title": "Music: The 90s Grunge Scene",
        "category": "Music",
        "questions": [
            {"text": "Who was the lead singer of Nirvana?", "options": ["Eddie Vedder", "Chris Cornell", "Kurt Cobain", "Layne Staley"], "answer": "Kurt Cobain", "fact": "Cobain founded Nirvana in Aberdeen, Washington.", "difficulty": "easy", "order": 1},
            {"text": "Which album did Pearl Jam release in 1991?", "options": ["Nevermind", "Ten", "Dirt", "Superunknown"], "answer": "Ten", "fact": "Ten featured hits like 'Alive' and 'Jeremy'.", "difficulty": "medium", "order": 2},
            {"text": "What city is credited as the birthplace of Grunge?", "options": ["Portland", "Seattle", "Olympia", "Tacoma"], "answer": "Seattle", "fact": "The 'Seattle Sound' defined the early 90s rock scene.", "difficulty": "easy", "order": 3},
            {"text": "Which band released 'Black Hole Sun'?", "options": ["Alice in Chains", "Stone Temple Pilots", "Soundgarden", "The Smashing Pumpkins"], "answer": "Soundgarden", "fact": "Soundgarden was led by Chris Cornell.", "difficulty": "medium", "order": 4},
            {"text": "What was Nirvana's debut studio album released in 1989?", "options": ["Bleach", "In Utero", "Incesticide", "Nevermind"], "answer": "Bleach", "fact": "Bleach was released on the Sub Pop label.", "difficulty": "hard", "order": 5}
        ]
    },
    {
        "title": "Tech: AI & Future Tech",
        "category": "Tech",
        "questions": [
            {"text": "What does GPT stand for?", "options": ["General Purpose Tech", "Generative Pre-trained Transformer", "Global Processing Tool", "Giant Parallel Translator"], "answer": "Generative Pre-trained Transformer", "fact": "GPT is the architecture behind ChatGPT.", "difficulty": "medium", "order": 1},
            {"text": "In what year was Bitcoin created?", "options": ["2007", "2008", "2009", "2010"], "answer": "2009", "fact": "Bitcoin was launched by someone under the name Satoshi Nakamoto.", "difficulty": "medium", "order": 2},
            {"text": "Which company developed the 'AlphaGo' AI?", "options": ["Google DeepMind", "OpenAI", "Meta", "IBM"], "answer": "Google DeepMind", "fact": "AlphaGo defeated a world champion Go player in 2016.", "difficulty": "medium", "order": 3},
            {"text": "What is the name of the first humanoid robot to receive citizenship?", "options": ["Sophia", "Atlas", "Asimo", "Pepper"], "answer": "Sophia", "fact": "Sophia was granted citizenship by Saudi Arabia.", "difficulty": "easy", "order": 4},
            {"text": "Who is the CEO of NVIDIA?", "options": ["Jensen Huang", "Tim Cook", "Satya Nadella", "Lisa Su"], "answer": "Jensen Huang", "fact": "He is often seen wearing a iconic black leather jacket.", "difficulty": "easy", "order": 5}
        ]
    }
]

def import_to_supabase():
    env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\kwizz\.env.local"
    load_dotenv(env_path)
    
    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not service_key:
        print("Missing Supabase config")
        return

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json"
    }
    
    base_url = f"{supabase_url}/rest/v1"

    try:
        import_count = 0
        for pack in QUIZ_PACKS:
            # Check if quiz exists
            r = httpx.get(f"{base_url}/quizzes?title=eq.{pack['title']}&select=id", headers=headers)
            if r.json():
                print(f"Skipping {pack['title']} (already exists)")
                continue

            # 1. Insert Quiz
            r = httpx.post(f"{base_url}/quizzes", headers={**headers, "Prefer": "return=representation"}, json={
                "title": pack['title'],
                "category": pack['category']
            })
            quiz_id = r.json()[0]['id']
            
            # 2. Insert Questions
            questions_to_insert = []
            for q in pack['questions']:
                questions_to_insert.append({
                    "quiz_id": quiz_id,
                    "text": q['text'],
                    "type": "multiple_choice",
                    "options": q['options'],
                    "answer": q['answer'],
                    "fact": q['fact'],
                    "difficulty": q['difficulty'],
                    "question_order": q['order']
                })
            
            httpx.post(f"{base_url}/questions", headers=headers, json=questions_to_insert)
            import_count += len(questions_to_insert)
                
        print(f"Successfully imported {import_count} questions into Kwizz DB via REST.")
    except Exception as e:
        print(f"Import failed: {e}")

if __name__ == "__main__":
    import_to_supabase()
