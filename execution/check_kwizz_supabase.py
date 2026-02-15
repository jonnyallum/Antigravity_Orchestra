"""
Kwizz Supabase Health Check (SOP Standardized)
Fixed for Windows: Removed emojis, standardized env paths.
"""

import os
import httpx
from dotenv import load_dotenv

def check_kwizz_supabase():
    # Standard env path
    env_path = r"c:\Users\jonny\Desktop\AgOS 3.0 template\Clients\kwizz\.env"
    load_dotenv(env_path)

    supabase_url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    anon_key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not anon_key:
        print("[ERROR] Missing NEXT_PUBLIC_SUPABASE_URL or NEXT_PUBLIC_SUPABASE_ANON_KEY in .env")
        return

    # Use service role key if available for full access, otherwise anon
    api_key = service_key or anon_key
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
    }

    base = f"{supabase_url}/rest/v1"
    tables = ["quizzes", "questions", "games", "players", "responses", "hosts"]

    print(f"[CONNECT] Connecting to Kwizz Supabase (REST API)...")
    print(f"   URL: {supabase_url}")
    print(f"   Key: {'service_role' if service_key else 'anon'}")
    print()

    all_ok = True
    for table in tables:
        try:
            # Use HEAD with Prefer: count=exact to get row count
            resp = httpx.get(
                f"{base}/{table}?select=id&limit=1",
                headers={**headers, "Prefer": "count=exact"},
                timeout=10,
            )
            if resp.status_code in (200, 206):
                content_range = resp.headers.get("content-range", "")
                if "/" in content_range:
                    count = content_range.split("/")[1]
                else:
                    count = str(len(resp.json()))
                print(f"  [OK] Table '{table}' -- {count} rows")
            elif resp.status_code == 404:
                print(f"  [WARN] Table '{table}' -- NOT FOUND (404)")
                all_ok = False
            else:
                print(f"  [FAIL] Table '{table}' -- HTTP {resp.status_code}: {resp.text[:100]}")
                all_ok = False
        except Exception as e:
            print(f"  [ERROR] Table '{table}' -- Error: {e}")
            all_ok = False

    print()
    if all_ok:
        print("[SUCCESS] Supabase is online and operational. All core tables accessible.")
    else:
        print("[ALERT] Some tables had issues. Check database schema and RLS policies.")

if __name__ == "__main__":
    check_kwizz_supabase()
