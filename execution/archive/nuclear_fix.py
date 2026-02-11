
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

# Nuclear option: Create the function in EVERY possible schema that PostgREST might look at
sql_nuclear = """
-- Drop existing to avoid conflicts
DROP FUNCTION IF EXISTS public.submit_lead_v2(text);

-- Create in public with explicit SECURITY DEFINER and proper grants
CREATE OR REPLACE FUNCTION public.submit_lead_v2(email_input text)
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

-- Revoke all first
REVOKE ALL ON FUNCTION public.submit_lead_v2(text) FROM PUBLIC;

-- Grant explicitly to the roles PostgREST uses
GRANT EXECUTE ON FUNCTION public.submit_lead_v2(text) TO anon;
GRANT EXECUTE ON FUNCTION public.submit_lead_v2(text) TO authenticated;
GRANT EXECUTE ON FUNCTION public.submit_lead_v2(text) TO service_role;

-- Update function ownership to postgres (ensures it has full rights)
ALTER FUNCTION public.submit_lead_v2(text) OWNER TO postgres;

-- Force PostgREST to reload
NOTIFY pgrst, 'reload schema';
NOTIFY pgrst, 'reload config';
"""

print("Applying nuclear fix...")
try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(sql_nuclear)
    conn.commit()
    print("SUCCESS: Function recreated with explicit permissions")
    conn.close()
except Exception as e:
    print(f"ERROR: {e}")
