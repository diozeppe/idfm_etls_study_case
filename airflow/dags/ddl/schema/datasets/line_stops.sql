CREATE TABLE IF NOT EXISTS line_stops (
    id              TEXT,
    route_long_name TEXT,
    stop_id         TEXT,
    stop_name       TEXT,
    stop_lon        TEXT,
    stop_lat        TEXT,
    operator_name   TEXT,
    short_name      TEXT,
    mode            TEXT,
    stop_geopoint   GEOGRAPHY(POINT, 4326),
    town            TEXT,
    code_insee      TEXT 
);

CREATE INDEX IF NOT EXISTS idx_line_stops_id_btree ON line_stops (id);