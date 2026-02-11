
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql = """
-- Ensure api schema exists
CREATE SCHEMA IF NOT EXISTS api;

-- Drop if exists
DROP FUNCTION IF EXISTS api.submit_lead_v2(text);

-- Create in the API schema (where PostgREST is looking!)
CREATE OR REPLACE FUNCTION api.submit_lead_v2(email_input text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.leads (email) 
  VALUES (email_input)
  ON CONFLICT (email) DO NOTHING;
  
  RETURN json_build_object('status', 'success', 'email', email_input);
EXCEPTION WHEN OTHERS THEN
  RETURN json_build_object('status', 'error', 'message', SQLERRM);
END;
$$;

-- Grant to PostgREST roles
GRANT USAGE ON SCHEMA api TO anon, authenticated, service_role;
GRANT EXECUTE ON FUNCTION api.submit_lead_v2(text) TO anon, authenticated, service_role;

-- Reload
NOTIFY pgrst, 'reload schema';
"""

print("Creating function in API schema (where PostgREST looks)...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("SUCCESS")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
