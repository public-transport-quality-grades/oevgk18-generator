#!/bin/sh

./scripts/osm-scripts/import-routing-data.sh

cat /post-import-sql/osm-import/* | psql -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db -f -