#!/bin/sh

raster2pgsql -s 2056 -d -I -C -M "$1" -t 128x128 public.terrain_model | psql -U "$POSTGRES_USER" -q "$POSTGRES_DB" -h db -f -