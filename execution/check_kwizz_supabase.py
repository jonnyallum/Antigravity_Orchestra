"""
Kwizz Supabase Health Check
Self-annealed: 2026-02-06 — Switched from direct PostgreSQL (DNS fails on free-tier)
to REST API via httpx, which is what the app and MCP actually use.
"""

import os
import httpx
from dotenv import load_dotenv

def check_kwizz_supabase():
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env.local"
    load_dotenv(env_path)

    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    anon_key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not anon_key:
        print("❌ Error: Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY in .env.local")
        return

    # Use service role key if available for full access, otherwise anon
    api_key = service_key or anon_key
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
    }

    base = f"{supabase_url}/rest/v1"
    tables = ["quizzes", "questions", "games", "players"]

    print(f"🔗 Connecting to Kwizz Supabase (REST API)...")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {'service_role' if service_key else 'anon'}")
    print()

    all_ok = True
    for table in tables:
        try:
            # Use HEAD with Prefer: count=exact to get row count without downloading data
            resp = httpx.get(
                f"{base}/{table}?select=id&limit=1",
                headers={**headers, "Prefer": "count=exact"},
                timeout=10,
            )
            if resp.status_code in (200, 206):
                # 200 = full result, 206 = partial content (limit applied)
                # Extract count from content-range header
                content_range = resp.headers.get("content-range", "")
                if "/" in content_range:
                    count = content_range.split("/")[1]
                else:
                    count = str(len(resp.json()))
                print(f"  ✅ Table '{table}' — {count} rows")
            elif resp.status_code == 404:
                print(f"  ⚠️  Table '{table}' — NOT FOUND (404)")
                all_ok = False
            else:
                print(f"  ❌ Table '{table}' — HTTP {resp.status_code}: {resp.text[:100]}")
                all_ok = False
        except Exception as e:
            print(f"  ❌ Table '{table}' — Error: {e}")
            all_ok = False

    print()
    if all_ok:
        print("🎤 Supabase is SINGING! All tables accessible via REST API.")
    else:
        print("⚠️  Some tables had issues. Check Supabase dashboard.")

if __name__ == "__main__":
    check_kwizz_supabase()
