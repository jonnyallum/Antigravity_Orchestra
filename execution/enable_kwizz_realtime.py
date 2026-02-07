"""Enable Supabase Realtime for Kwizz tables via direct SQL"""
import psycopg2

# URL-decoded password: Aprilia100!69.
conn = psycopg2.connect(
    host="db.japkqygktnubcrmlttqt.supabase.co",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="Aprilia100!69."
)
conn.autocommit = True
cur = conn.cursor()

tables = ['games', 'players', 'responses']
for table in tables:
    try:
        cur.execute(f"ALTER PUBLICATION supabase_realtime ADD TABLE {table};")
        print(f"✅ Added {table} to supabase_realtime")
    except Exception as e:
        if 'already member' in str(e).lower() or 'already exists' in str(e).lower():
            print(f"ℹ️  {table} already in supabase_realtime")
        else:
            print(f"⚠️  {table}: {e}")

# Verify
cur.execute("SELECT tablename FROM pg_publication_tables WHERE pubname = 'supabase_realtime';")
rows = cur.fetchall()
print(f"\n📡 Tables in supabase_realtime publication:")
for row in rows:
    print(f"  - {row[0]}")

cur.close()
conn.close()
print("\n✅ Done!")
