#!/bin/sh

mkdir pgimport

osmosis --read-pbf $1 \
    --tf accept-nodes uic_ref=*\
    --tf reject-ways \
    --tf reject-relations \
    --write-pgsql-dump

mkdir -p /sql-import/pt-stop-data
mv pgimport/* /sql-import/pt-stop-data
rm -R pgimport