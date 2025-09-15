CREATE TABLE IF NOT EXISTS api_data (
    id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    run_date DATE NOT NULL DEFAULT CURRENT_DATE,
    inserted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    payload JSONB NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_api_data_source_date ON api_data(source_name,
                run_date);