CREATE TABLE IF NOT EXISTS operators (
    id                      TEXT PRIMARY KEY,
    name                    TEXT,
    street_number           TEXT,
    address                 TEXT,
    address_additional_info TEXT,
    town                    TEXT,
    post_code               VARCHAR(5),
    post_code_extension     TEXT,
    phone                   TEXT,
    url                     TEXT,
    addtional_details       TEXT,
    contact                 TEXT,
    logo                    TEXT,
    email                   TEXT
);

CREATE INDEX IF NOT EXISTS idx_operators_id_btree ON operators (id);
