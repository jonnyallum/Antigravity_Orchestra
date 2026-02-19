
import psycopg2

DB_URL = "postgresql://postgres.kerqqobkiziadwtkpprx:Aprilia100!69.@aws-1-eu-west-2.pooler.supabase.com:6543/postgres"

sql = """
-- 1. Ensure table exists
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Force Grants (Critical for API visibility)
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT ALL ON TABLE public.leads TO anon, authenticated, service_role;

-- 3. Enable RLS
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;

-- 4. Policies (Drop and Recreate to be sure)
DROP POLICY IF EXISTS "Enable insert for anon" ON public.leads;
CREATE POLICY "Enable insert for anon" ON public.leads FOR INSERT TO anon WITH CHECK (true);

-- 5. Notify
NOTIFY pgrst, 'reload config';
"""

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print("Executing SQL Fixes...")
    cur.execute(sql)
    conn.commit()
    print("SUCCESS: Table fixes and Grants applied.")
except Exception as e:
    print(f"SQL ERROR: {e}")
    # Try non-transaction mode?
finally:
   if 'conn' in locals() and conn: conn.close()
