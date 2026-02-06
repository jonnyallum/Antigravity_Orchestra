
-- Antigravity Betting Hub Schema (AgOS 3.0)

-- 1. Fixtures (Raw data for the next 48h)
CREATE TABLE IF NOT EXISTS bet_fixtures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sport TEXT NOT NULL, -- 'football' or 'horse_racing'
    event_name TEXT NOT NULL,
    start_time TIMESTAMPTZ NOT NULL,
    venue TEXT,
    market_data JSONB, -- Odds, weather, etc.
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Predictions (The "test bets")
CREATE TABLE IF NOT EXISTS bet_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fixture_id UUID REFERENCES bet_fixtures(id) ON DELETE CASCADE,
    prediction_type TEXT NOT NULL, -- 'accumulator', 'goalscorer', 'win', 'tricast'
    prediction_data JSONB NOT NULL, -- The actual pick details
    algorithm_version TEXT DEFAULT 'v1.0',
    conviction_score FLOAT, -- 0-1
    is_verified_by_redeye BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    result_status TEXT DEFAULT 'pending' -- 'pending', 'win', 'loss', 'void'
);

-- 3. Results (Final outcomes)
CREATE TABLE IF NOT EXISTS bet_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id UUID REFERENCES bet_predictions(id) ON DELETE CASCADE,
    actual_outcome TEXT,
    profit_loss FLOAT,
    settled_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Performance Logs (Success rates)
CREATE TABLE IF NOT EXISTS bet_performance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    algorithm_version TEXT,
    sport TEXT,
    total_bets INT DEFAULT 0,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    roi FLOAT DEFAULT 0,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Realtime
ALTER PUBLICATION supabase_realtime ADD TABLE bet_predictions;
ALTER PUBLICATION supabase_realtime ADD TABLE bet_performance;
