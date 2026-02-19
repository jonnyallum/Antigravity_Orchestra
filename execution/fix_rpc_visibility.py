
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql = """
-- 1. Create Schema if missing
CREATE SCHEMA IF NOT EXISTS api;

-- 2. Create the function in 'api' schema (Proxy)
CREATE OR REPLACE FUNCTION api.submit_lead(email_input text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- Call the public function or just insert directly
  INSERT INTO public.leads (email) VALUES (email_input);
  RETURN json_build_object('status', 'ok', 'email', email_input);
END;
$$;

-- 3. Grants
GRANT USAGE ON SCHEMA api TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION api.submit_lead(text) TO anon, authenticated, service_role;

-- 4. Reload
NOTIFY pgrst, 'reload config';
"""

print("Creating api.submit_lead proxy...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("SUCCESS.")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
