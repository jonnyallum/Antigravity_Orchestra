
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load Env
ENV_PATH = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
load_dotenv(ENV_PATH)
URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(URL, KEY)

# Categorization Map (Unified Taxonomy)
TAXONOMY_MAP = {
    # OpenTDB Mappings
    "Science & Nature": "Science",
    "Science: Computers": "Technology",
    "Science: Mathematics": "Science",
    "Science: Gadgets": "Technology",
    "Entertainment: Music": "Music",
    "Entertainment: Video Games": "Gaming",
    "Entertainment: Film": "Movies",
    "Entertainment: Television": "TV",
    "Entertainment: Board Games": "Gaming",
    "Entertainment: Comics": "Pop Culture",
    "Entertainment: Anime & Manga": "Pop Culture",
    "Entertainment: Cartoon & Animations": "Pop Culture",
    "Entertainment: Books": "Literature",
    "Entertainment: Musical & Theatres": "Arts",
    "Animals": "Nature",
    "General Knowledge": "General",
    "Mythology": "History",
    "Geography": "Geography",
    "History": "History",
    "Politics": "History",
    "Art": "Arts",
    "Celebrities": "Pop Culture",
    "Sports": "Sports",
    "Vehicles": "Technology",
    
    # jService / Other
    "General": "General",
    "niche": "Specialized",
    "AI": "Technology"
}

def align_taxonomy():
    print("[TAXONOMY] Fetching all quizzes for alignment...")
    res = supabase.table("quizzes").select("id, title, category").execute()
    quizzes = res.data
    
    updates = 0
    for q in quizzes:
        cat = q['category']
        new_cat = TAXONOMY_MAP.get(cat)
        
        # If we have a mapping or need cleanup
        if new_cat and new_cat != cat:
            print(f"Mapping: '{cat}' -> '{new_cat}' for Quiz: {q['title']}")
            supabase.table("quizzes").update({"category": new_cat}).eq("id", q['id']).execute()
            updates += 1
            
    print(f"[SUCCESS] Taxonomy Alignment complete. {updates} quizzes updated.")

if __name__ == "__main__":
    align_taxonomy()
