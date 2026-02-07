
import os
import asyncio
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize FastMCP server
mcp = FastMCP("Kwizz Supabase")

# Load environment variables
env_path = r"c:\Users\jonny\Desktop\Jai.OS 4.0 template\Clients\kwizz\.env.local"
load_dotenv(env_path)

supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials in .env.local")

supabase: Client = create_client(supabase_url, supabase_key)

@mcp.tool()
async def list_quizzes(category: Optional[str] = None) -> str:
    """List all available quiz packs."""
    query = supabase.from_("quizzes").select("id, title, category")
    if category:
        query = query.eq("category", category)
    
    result = query.execute()
    if not result.data:
        return "No quizzes found."
    
    output = "Available Quizzes:\n"
    for q in result.data:
        output += f"- [{q['category']}] {q['title']} (ID: {q['id']})\n"
    return output

@mcp.tool()
async def get_quiz_details(quiz_id: str) -> str:
    """Get all questions for a specific quiz pack."""
    quiz_res = supabase.from_("quizzes").select("*").eq("id", quiz_id).single().execute()
    if not quiz_res.data:
        return f"Quiz {quiz_id} not found."
    
    questions_res = supabase.from_("questions").select("*").eq("quiz_id", quiz_id).order("question_order").execute()
    
    output = f"Quiz: {quiz_res.data['title']} ({quiz_res.data['category']})\n"
    output += "=" * 40 + "\n"
    for q in questions_res.data:
        output += f"Q{q['question_order']}: {q['text']}\n"
        output += f"Options: {', '.join(q['options'])}\n"
        output += f"Answer: {q['answer']}\n"
        if q.get('fact'):
            output += f"Fact: {q['fact']}\n"
        output += "-" * 20 + "\n"
    return output

@mcp.tool()
async def create_quiz_pack(title: str, category: str, questions: List[dict]) -> str:
    """
    Create a new quiz pack.
    Questions list should contain dicts with: text, options (list), answer, fact (optional), difficulty, order.
    """
    # 1. Insert Quiz
    quiz_res = supabase.from_("quizzes").insert({"title": title, "category": category}).execute()
    if not quiz_res.data:
        return "Failed to create quiz pack."
    
    quiz_id = quiz_res.data[0]['id']
    
    # 2. Insert Questions
    question_data = []
    for q in questions:
        question_data.append({
            "quiz_id": quiz_id,
            "text": q['text'],
            "type": q.get('type', 'multiple_choice'),
            "options": q['options'],
            "answer": q['answer'],
            "fact": q.get('fact'),
            "difficulty": q.get('difficulty', 'medium'),
            "question_order": q['order']
        })
    
    q_res = supabase.from_("questions").insert(question_data).execute()
    if not q_res.data:
        return f"Created quiz {quiz_id} but failed to insert questions."
    
    return f"Successfully created quiz pack '{title}' with {len(q_res.data)} questions. ID: {quiz_id}"

@mcp.tool()
async def get_active_games() -> str:
    """List all currently active game sessions."""
    res = supabase.from_("games").select("*, quizzes(title)").neq("status", "finished").execute()
    if not res.data:
        return "No active games."
    
    output = "Active Games:\n"
    for g in res.data:
        output += f"- PIN: {g['pin']} | Status: {g['status']} | Quiz: {g['quizzes']['title']}\n"
    return output

if __name__ == "__main__":
    mcp.run()
