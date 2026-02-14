
import os
import asyncio
from typing import Optional, List
from mcp.server.fastmcp import FastMCP
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize FastMCP server
mcp = FastMCP("Kwizz Supabase")

# Load environment variables
env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env.local"
load_dotenv(env_path)

supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials in .env.local")

supabase: Client = create_client(supabase_url, supabase_key)

@mcp.tool()
async def get_billing_status(host_email: str) -> str:
    """Check host credit balance and subscription status."""
    host_res = supabase.from_("hosts").select("*").eq("email", host_email).single().execute()
    if not host_res.data:
        return f"No host found for email {host_email}"
    
    host_id = host_res.data['id']
    credits_res = supabase.from_("host_credits").select("credits_remaining").eq("host_id", host_id).execute()
    total_credits = sum(c['credits_remaining'] for c in credits_res.data) if credits_res.data else 0
    
    sub_res = supabase.from_("host_subscriptions").select("*").eq("host_id", host_id).eq("status", "active").execute()
    sub_status = "Active Unlimited Plan" if sub_res.data else "No active subscription"
    
    return f"Host: {host_res.data['display_name']}\nFree Credits: {host_res.data['free_credits_remaining']}\nPaid Credits: {total_credits}\nSubscription: {sub_status}"

@mcp.tool()
async def create_host(display_name: str, email: str, venue_name: Optional[str] = None) -> str:
    """Initialize a new host record with 3 free trial credits."""
    data = {
        "display_name": display_name,
        "email": email,
        "venue_name": venue_name,
        "free_credits_remaining": 3
    }
    res = supabase.from_("hosts").insert(data).execute()
    if not res.data:
        return "Failed to create host."
    return f"Successfully created host '{display_name}' (ID: {res.data[0]['id']}) with 3 free credits."

@mcp.tool()
async def add_credits(host_id: str, amount: int, pack_type: str = "single") -> str:
    """Manually add credits to a host account (Admin). pack_type: single, ten_pack, fifty_two_pack."""
    data = {
        "host_id": host_id,
        "credits_purchased": amount,
        "credits_remaining": amount,
        "pack_type": pack_type,
        "amount_paid_pence": 0 # Admin override
    }
    res = supabase.from_("host_credits").insert(data).execute()
    if not res.data:
        return "Failed to add credits."
    return f"Successfully added {amount} credits to host {host_id}."

@mcp.tool()
async def get_sponsor_rounds(category: Optional[str] = None) -> str:
    """List active sponsor rounds, optionally filtered by category."""
    query = supabase.from_("sponsor_rounds").select("*").eq("is_active", True)
    res = query.execute()
    if not res.data:
        return "No active sponsors found."
    
    sponsors = res.data
    if category:
        sponsors = [s for s in sponsors if not s['target_categories'] or category in s['target_categories']]
    
    output = "Active Sponsors:\n"
    for s in sponsors:
        output += f"- {s['brand_name']}: {s['round_title']} (Code: {s['discount_code']})\n"
    return output

@mcp.tool()
async def get_player_prime_profile(user_id: str) -> str:
    """View a player's cosmetic selections and game stats."""
    res = supabase.from_("player_prime").select("*").eq("user_id", user_id).single().execute()
    if not res.data:
        return f"No Prime profile found for user {user_id}"
    
    p = res.data
    output = f"Player Prime Profile ({p['tier']})\n"
    output += f"Buzzer: {p['buzzer_sound']} | Avatar: {p['avatar_style']} | Entry: {p['entry_animation']}\n"
    output += f"Stats: {p['total_wins']} Wins / {p['total_games_played']} Played (Best Streak: {p['best_streak']})\n"
    output += f"Fastest Reaction: {p['fastest_buzz_ms']}ms"
    return output

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
