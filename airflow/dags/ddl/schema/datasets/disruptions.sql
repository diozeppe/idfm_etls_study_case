CREATE TABLE IF NOT EXISTS disruptions (
    id TEXT PRIMARY KEY,
    application_periods JSONB,
    last_update TIMESTAMP,
    cause TEXT,
    severity TEXT,
    title TEXT,
    message TEXT,
    short_message TEXT,
    tags TEXT[],
    affected_objects TEXT[]
);

CREATE INDEX IF NOT EXISTS idx_disruptions_id_btree ON disruptions (id);