
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

# Check current PostgREST configuration
sql_check = """
SELECT name, setting 
FROM pg_settings 
WHERE name LIKE '%pgrst%' OR name LIKE '%search_path%';
"""

# Get all schemas
sql_schemas = """
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name NOT LIKE 'pg_%' 
  AND schema_name != 'information_schema';
"""

# Check if our function exists and is visible
sql_functions = """
SELECT 
    n.nspname as schema,
    p.proname as function_name,
    pg_get_function_identity_arguments(p.oid) as arguments
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE p.proname LIKE '%submit_lead%'
ORDER BY n.nspname, p.proname;
"""

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("=== POSTGREST CONFIGURATION ===")
    cur.execute(sql_check)
    for row in cur.fetchall():
        print(f"{row[0]}: {row[1]}")
    
    print("\n=== ALL SCHEMAS ===")
    cur.execute(sql_schemas)
    for row in cur.fetchall():
        print(f"- {row[0]}")
    
    print("\n=== SUBMIT_LEAD FUNCTIONS ===")
    cur.execute(sql_functions)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"{row[0]}.{row[1]}({row[2]})")
    else:
        print("No functions found!")
    
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
