
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql_expose = """
-- Create the api schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS api;

-- Create a VIEW in the api schema that points to the public table
CREATE OR REPLACE VIEW api.leads AS SELECT * FROM public.leads;

-- Grant permissions on the schema and view
GRANT USAGE ON SCHEMA api TO anon, authenticated, service_role;
GRANT SELECT, INSERT ON api.leads TO anon, authenticated, service_role;

-- Ensure public table is accessible
GRANT ALL ON public.leads TO anon, authenticated, service_role;

NOTIFY pgrst, 'reload config';
"""

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print("Exposing 'public.leads' via 'api.leads' VIEW...")
    cur.execute(sql_expose)
    conn.commit()
    print("SUCCESS: View created and exposed.")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
