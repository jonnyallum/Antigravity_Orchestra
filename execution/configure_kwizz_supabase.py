'' """
Configure Kwizz Supabase project:
1. Set Auth URL config (Site URL + Redirect URLs)
2. Enable Realtime for games/players/responses tables
"""
import requests
import json

# Kwizz Supabase project
PROJECT_REF = "japkqygktnubcrmlttqt"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImphcGtxeWdrdG51YmNybWx0dHF0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDE2MTk3OCwiZXhwIjoyMDg1NzM3OTc4fQ.jE8j8FjQyqWkw8DtHHAjgYaNNKj_MjH5IUa2tUq2aUY"
SUPABASE_URL = f"https://{PROJECT_REF}.supabase.co"

# ============================================================
# TASK 1: Enable Realtime via SQL (using the REST API with service role)
# ============================================================
print("=" * 60)
print("TASK 1: Enable Realtime for tables")
print("=" * 60)

# Use the Supabase REST API to run SQL via RPC
# First, let's try using the PostgREST rpc endpoint
headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Enable realtime for each table by adding to the publication
tables = ['games', 'players', 'responses']

for table in tables:
    sql = f"ALTER PUBLICATION supabase_realtime ADD TABLE public.{table};"
    
    # Use the Supabase SQL endpoint (management API)
    # Since we can't use management API without access token, 
    # let's use the database connection via psycopg2 with the pooler
    print(f"  Preparing: {table}...")

# Try direct connection via Supabase pooler (port 6543)
try:
    import psycopg2
    
    # Use the transaction pooler (port 6543) instead of direct connection (port 5432)
    # which is more likely to work
    conn = psycopg2.connect(
        host=f"aws-0-eu-west-2.pooler.supabase.com",
        port=6543,
        dbname="postgres",
        user=f"postgres.{PROJECT_REF}",
        password="Aprilia100!69.",
        connect_timeout=10
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    for table in tables:
        try:
            cur.execute(f"ALTER PUBLICATION supabase_realtime ADD TABLE public.{table};")
            print(f"  ✅ Added {table} to supabase_realtime")
        except Exception as e:
            err_str = str(e).lower()
            if 'already member' in err_str or 'already exists' in err_str:
                print(f"  ℹ️  {table} already in supabase_realtime")
                conn.rollback()
            else:
                print(f"  ⚠️  {table}: {e}")
                conn.rollback()
    
    # Verify
    cur.execute("SELECT tablename FROM pg_publication_tables WHERE pubname = 'supabase_realtime';")
    rows = cur.fetchall()
    print(f"\n  📡 Tables in supabase_realtime publication:")
    for row in rows:
        print(f"    - {row[0]}")
    
    cur.close()
    conn.close()
    print("  ✅ Realtime configuration complete!")
    
except ImportError:
    print("  ⚠️  psycopg2 not available, trying REST API approach...")
except Exception as e:
    print(f"  ⚠️  Database connection failed: {e}")
    print("  Trying REST API approach...")

# ============================================================
# TASK 2: Update Auth URL Configuration via Supabase Management API
# ============================================================
print("\n" + "=" * 60)
print("TASK 2: Update Auth URL Configuration")
print("=" * 60)

# The Supabase Management API requires a personal access token or 
# we can update auth config via the GoTrue admin endpoint
# Let's use the GoTrue admin API which accepts the service role key

gotrue_url = f"{SUPABASE_URL}/auth/v1"
admin_headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

# Check current auth settings
print("\n  Checking current auth config...")
try:
    # The GoTrue admin API doesn't expose config directly
    # We need to use the Supabase Management API for URL config
    # This requires a Supabase access token (from dashboard login)
    
    # Alternative: Use the Supabase Management API v1
    # First, let's check if we can access it
    mgmt_url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/config/auth"
    
    # Try with service role key (may not work - management API needs personal access token)
    resp = requests.get(mgmt_url, headers={
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "Content-Type": "application/json"
    })
    
    if resp.status_code == 200:
        config = resp.json()
        print(f"  Current Site URL: {config.get('SITE_URL', 'not set')}")
        print(f"  Current Redirect URLs: {config.get('URI_ALLOW_LIST', 'not set')}")
        
        # Update the config
        update_data = {
            "SITE_URL": "https://kwizz.co.uk",
            "URI_ALLOW_LIST": "https://kwizz.co.uk/auth/callback,https://kwizz.co.uk/**,http://localhost:3000/auth/callback"
        }
        
        resp2 = requests.patch(mgmt_url, headers={
            "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        }, json=update_data)
        
        if resp2.status_code == 200:
            print("  ✅ Auth URL config updated successfully!")
            print(f"    Site URL: https://kwizz.co.uk")
            print(f"    Redirect URLs: https://kwizz.co.uk/auth/callback")
        else:
            print(f"  ⚠️  Management API returned {resp2.status_code}: {resp2.text}")
            print("  → You may need to set this manually in Supabase Dashboard")
    else:
        print(f"  ⚠️  Management API returned {resp.status_code}")
        print("  The Management API requires a Supabase personal access token.")
        print("  Trying alternative approach...")
        
        # Alternative: Generate a Supabase access token
        # Check if we have one in .env or can use the dashboard API
        print("\n  📋 MANUAL STEPS REQUIRED for Auth URL Config:")
        print("  ─────────────────────────────────────────────")
        print("  1. Go to: https://supabase.com/dashboard/project/japkqygktnubcrmlttqt/auth/url-configuration")
        print("  2. Set Site URL to: https://kwizz.co.uk")
        print("  3. Add Redirect URLs:")
        print("     - https://kwizz.co.uk/auth/callback")
        print("     - https://kwizz.co.uk/**")
        print("     - http://localhost:3000/auth/callback")
        print("  4. Click Save")
        
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
