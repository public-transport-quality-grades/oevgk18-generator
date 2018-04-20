#!/bin/sh

set -e

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db <<-EOSQL
    TRUNCATE agency CASCADE;
    TRUNCATE stops CASCADE;
    TRUNCATE calendar CASCADE;
    TRUNCATE calendar_dates CASCADE;
	\copy agency from sql-import/gtfs-data/agency.txt with csv header
    \copy stops from sql-import/gtfs-data/stops.txt with csv header
    \copy routes from sql-import/gtfs-data/routes.txt with csv header
    \copy calendar from sql-import/gtfs-data/calendar.txt with csv header
    \copy calendar_dates from sql-import/gtfs-data/calendar_dates.txt with csv header
    \copy trips from sql-import/gtfs-data/trips.txt with csv header
    \copy stop_times from sql-import/gtfs-data/stop_times.txt with csv header
    \copy transfers from sql-import/gtfs-data/transfers.txt with csv header
    \copy frequencies from sql-import/gtfs-data/frequencies.txt with csv header
EOSQL

cat /post-import-sql/gtfs-import/* | psql -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db -f -