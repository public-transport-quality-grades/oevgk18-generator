#!/bin/sh

mkdir pgimport

osmosis --read-xml $1 \
    --tf accept-nodes public_transport=stop_position highway=bus_stop \
    --tf reject-ways \
    --tf reject-relations \
    --write-pgsql-dump

mkdir -p /sql-import/pt-stop-data
mv pgimport/* /sql-import/pt-stop-data
rm -R pgimport