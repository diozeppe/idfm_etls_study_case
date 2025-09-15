CREATE TABLE IF NOT EXISTS stops (
    id             TEXT PRIMARY KEY,
    version        TEXT,
    created        TIMESTAMP WITH TIME ZONE,
    changed        TIMESTAMP WITH TIME ZONE,
    name           TEXT,
    type           TEXT,
    publiccode     TEXT,
    xepsg2154      INTEGER,
    yepsg2154      INTEGER,
    town           TEXT,
    postalregion   TEXT,
    accessibility  TEXT,
    audiblesignals TEXT,
    visualsigns    TEXT,
    farezone       TEXT,
    zdaid          TEXT,
    geopoint       GEOGRAPHY(POINT, 4326)
);

CREATE INDEX IF NOT EXISTS idx_stop_id_btree ON stops (id);
