
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql = """
SELECT schema_name FROM information_schema.schemata;
"""

sql_tables = """
SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE table_name = 'leads';
"""

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("--- SCHEMAS ---")
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        print(r[0])
        
    print("\n--- TABLES named 'leads' ---")
    cur.execute(sql_tables)
    rows = cur.fetchall()
    for r in rows:
        print(f"{r[0]}.{r[1]}")
        
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
