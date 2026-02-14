import psycopg2
import sys

def main():
    PROJECT_REF = "japkqygktnubcrmlttqt"
    PASSWORD = "Aprilia100!69."
    DB_HOST = f"db.{PROJECT_REF}.supabase.co"
    
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=5432,
            dbname="postgres",
            user="postgres",
            password=PASSWORD,
            connect_timeout=10
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print(f"Connected to {DB_HOST}")
        
        # 1. Create hosts table
        print("Creating 'hosts' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hosts (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                email TEXT UNIQUE NOT NULL,
                display_name TEXT,
                venue_name TEXT,
                free_credits_remaining INT DEFAULT 3,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 2. Create host_credits table
        print("Creating 'host_credits' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS host_credits (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                host_id UUID REFERENCES hosts(id) ON DELETE CASCADE,
                credits_purchased INT NOT NULL,
                credits_remaining INT NOT NULL,
                pack_type TEXT,
                amount_paid_pence INT DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 3. Create host_subscriptions table
        print("Creating 'host_subscriptions' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS host_subscriptions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                host_id UUID REFERENCES hosts(id) ON DELETE CASCADE,
                status TEXT DEFAULT 'inactive',
                current_period_end TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 4. Create player_prime table
        print("Creating 'player_prime' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player_prime (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID UNIQUE NOT NULL,
                tier TEXT DEFAULT 'free',
                buzzer_sound TEXT DEFAULT 'default',
                avatar_style TEXT DEFAULT 'default',
                entry_animation TEXT DEFAULT 'none',
                total_wins INT DEFAULT 0,
                total_games_played INT DEFAULT 0,
                best_streak INT DEFAULT 0,
                fastest_buzz_ms INT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 5. Create sponsor_rounds table
        print("Creating 'sponsor_rounds' table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sponsor_rounds (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                brand_name TEXT NOT NULL,
                round_title TEXT NOT NULL,
                discount_code TEXT,
                image_url TEXT,
                target_categories TEXT[],
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)

        # 6. Enable Realtime for new tables (optional but useful for credits)
        print("Enabling Realtime for monetization tables...")
        for table in ["hosts", "host_credits"]:
            try:
                cur.execute(f"ALTER PUBLICATION supabase_realtime ADD TABLE public.{table};")
            except Exception as e:
                if "already member" in str(e).lower():
                    pass
                else:
                    print(f"  Warning adding {table} to realtime: {e}")

        print("\nMonetization Schema Initialized Successfully!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
