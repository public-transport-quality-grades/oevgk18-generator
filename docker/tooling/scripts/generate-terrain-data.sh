#!/bin/sh

raster2pgsql -s 2056 -d -I -C -M "$1" -t 128x128 public.swissalti3d > /sql-import/import-terrain-data.sql