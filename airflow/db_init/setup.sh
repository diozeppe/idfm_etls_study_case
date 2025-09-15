# Here we initialize our PostgresDB and install PostGis for the Geopoint/Geography data columns

#!/bin/sh
set -e

echo $POSTGRES_IDFM_DB

DB_NAME="$POSTGRES_IDFM_DB"
DB_USER="$POSTGRES_USER"

echo "Creating database '$DB_NAME' with owner '$DB_USER'..."

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
CREATE DATABASE $DB_NAME OWNER $DB_USER;
EOSQL

echo "Database '$DB_NAME' created."

echo "Installing PostGIS extensions..."
psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" <<-EOSQL
CREATE EXTENSION postgis;
EOSQL

echo "PostGIS enabled in '$DB_NAME'"
