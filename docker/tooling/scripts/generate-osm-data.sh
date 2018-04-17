#!/bin/sh

./scripts/osm-scripts/generate-routing-data.sh $1
./scripts/osm-scripts/generate-pt-stop-data.sh $1
