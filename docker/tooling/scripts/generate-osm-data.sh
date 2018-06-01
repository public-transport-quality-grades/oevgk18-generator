#!/bin/sh

if [[ "$#" -ne 1 ]]; then
    OSM_FOLDER=/osm-data/
    if [ ! -f $OSM_FOLDER/switzerland-exact.osm.pbf ]; then
        echo "No path to OSM file specified, downloading newest file for Switzerland from planet.osm.ch"
        wget -P $OSM_FOLDER https://planet.osm.ch/switzerland-exact.osm.pbf
    else
        echo "No path to OSM file specified, using switzerland-exact.osm.pbf"
    fi
    ./scripts/osm-scripts/generate-routing-data.sh $OSM_FOLDER/switzerland-exact.osm.pbf
else
    ./scripts/osm-scripts/generate-routing-data.sh $1
fi

