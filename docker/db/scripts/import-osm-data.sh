#!/bin/sh

./scripts/osm-scripts/import-routing-data.sh
./scripts/osm-scripts/import-pt-stop-data.sh

cat /post-import-sql/osm-import/* | psql -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db -f -