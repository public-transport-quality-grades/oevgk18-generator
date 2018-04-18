#!/bin/sh

set -e

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db <<-EOSQL
    TRUNCATE pt_stop CASCADE;
    ALTER TABLE pt_stop DROP CONSTRAINT pk_pt_stop;
    DROP INDEX idx_pt_stop_geom CASCADE;

    \copy pt_stop from sql-import/pt-stop-data/nodes.txt

    ALTER TABLE ONLY pt_stop ADD CONSTRAINT pk_pt_stop PRIMARY KEY (id);
    CREATE INDEX idx_pt_stop_geom ON pt_stop USING gist (geom);
    ALTER TABLE ONLY pt_stop CLUSTER ON idx_pt_stop_geom;
EOSQL