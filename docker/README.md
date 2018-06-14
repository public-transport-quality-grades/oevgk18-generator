# OeVGK18 Generator - Docker Setup

This setup with Docker is meant to get a database up and running and then generate the public transport gradings ("ÖV-Güteklassen") in Switzerland.
This process uses three Docker containers, `db`, `tooling` and `generator`. While `db` contains the database and scripts to setup the schemas, the `tooling` container prepares data for insertion into the database. The `generator` container is used to generate the gradings themselves.

The individual steps have to be executed in the order they appear here.

## Prerequisites
- [Docker](https://www.docker.com/community-edition#/download)
- [Docker Compose](https://docs.docker.com/compose/install/)
- OSM file (PBF format) of the desired region (from e.g. <https://planet.osm.ch/>)
- Terrain model of the region (GeoTIF format)

## Start environment

``` bash
docker-compose up -d
```

## Database setup

### Optional: Update intercity railway stations

Inside the [db](https://github.com/public-transport-quality-grades/oevgk18-generator/tree/master/docker/db) folder is a [csv file](https://github.com/public-transport-quality-grades/oevgk18-generator/blob/master/docker/db/intercity_railway_stations.csv) with all the railway stations which have an intercity connection.
If you wish to update this data, see the [README](https://github.com/public-transport-quality-grades/oevgk18-generator/tree/master/docker/db)

### Updating GTFS data

The first command automatically downloads the public transport schedule from <http://gtfs.geops.ch/>. The second commands imports sets up the database table and imports the timetable data.

``` bash
docker-compose run tooling generate-gtfs-data.sh
docker-compose run db import-gtfs-data.sh
```

### Updating OSM data

Make sure that the OSM file is placed under `docker/tooling/osm-data` and adjust the path in the command.

If no file is specified, data for Switzerland will be downloaded automatically.

``` bash
docker-compose run tooling generate-osm-data.sh /osm-data/<osm-filename>
docker-compose run db import-osm-data.sh
```

### Updating terrain data

Make sure the terrain-file is placed under `docker/db/terrain-data` and adjust the path in the command.

``` bash
docker-compose run db import-terrain-data.sh /terrain-data/<terrain-filename>
```

## Generating public transport stop gradings

After the database has been setup, the calculation of the gradings can begin:

```bash
docker-compose run generator oevgk18_generator
```

To see a usage guide of the command, simply run `docker-compose run generator`

The default configuration file is [generator/generator_config.yml](generator/generator_config.yml). The settings can be adjusted and the generator re-run with the same command.

After the command has been completed, the resulting files will be stored as GeoJSON inside the `generator/results` folder. To get a web application up and running with this data, see to the [web-app repository](https://github.com/public-transport-quality-grades/web-app)
