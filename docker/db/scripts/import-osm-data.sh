#!/bin/sh

psql -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db -f "/sql-import/import-osm-data.sql"