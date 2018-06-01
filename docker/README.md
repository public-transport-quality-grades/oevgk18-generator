# OeVGK18 Generator - Docker Setup

This setup with Docker is meant to get a database up and running and ready to generate the public transport ratings ("ÖV-Güteklassen") in Switzerland.
This process uses two Docker containers, `db` and `tooling`. While `db` contains the database and scripts to setup the schemas, the `tooling` container prepares data for insertion into the database.

The individual steps have to be executed in the order they appear here.

## Prerequisites
- [Docker](https://www.docker.com/community-edition#/download)
- [Docker Compose](https://docs.docker.com/compose/install/)
- OSM file (PBF format) of the desired region (from e.g. <https://planet.osm.ch/>)
- Terrain model of the region (GeoTIF format)

## Start database

``` bash
docker-compose up -d
```

## Updating GTFS data

The first command automatically downloads the public transport schedule from <http://gtfs.geops.ch/>. The second commands imports sets up the database table and imports the timetable data.

``` bash
docker-compose run tooling generate-gtfs-data.sh
docker-compose run db import-gtfs-data.sh
```

## Updating OSM data

Make sure that the OSM file is placed under `docker/tooling/osm-data` and adjust the path in the command.

If no file is specified, data for Switzerland will be downloaded automatically.

``` bash
docker-compose run tooling generate-osm-data.sh /osm-data/<osm-filename>
docker-compose run db import-osm-data.sh
```

## Updating terrain data

Make sure the terrain-file is placed under `docker/db/terrain-data` and adjust the path in the command.

``` bash
docker-compose run db import-terrain-data.sh /terrain-data/<terrain-filename>
```