#!/bin/sh

wget http://gtfs.geops.ch/dl/gtfs_complete.zip

mkdir /sql-import/gtfs-data
unzip gtfs_complete.zip -d /sql-import/gtfs-data -o
rm gtfs_complete.zip