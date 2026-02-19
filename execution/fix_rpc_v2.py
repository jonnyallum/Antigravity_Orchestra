
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql_fix_rpc = """
-- Drop the API schema function (avoid confusion)
DROP FUNCTION IF EXISTS api.submit_lead(text);

-- Recreate in PUBLIC schema (safest path)
CREATE OR REPLACE FUNCTION public.submit_lead_v2(email_input text)
RETURNS json
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  INSERT INTO public.leads (email) VALUES (email_input)
  ON CONFLICT (email) DO NOTHING;
  
  RETURN json_build_object('status', 'ok', 'email', email_input);
END;
$$;

-- Grant permissions explicitly
GRANT EXECUTE ON FUNCTION public.submit_lead_v2(text) TO anon, authenticated, service_role;

-- Notify
NOTIFY pgrst, 'reload config';
"""

print("Fixing RPC by moving to PUBLIC schema with v2 name...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql_fix_rpc)
    conn.commit()
    print("SUCCESS: public.submit_lead_v2 created.")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
