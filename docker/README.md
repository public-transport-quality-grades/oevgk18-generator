# oevgk18-generator docker

## start database

``` bash
docker-compose up
```

## updating osm data

Make sure that the osm-file is placed under /docker/tooling/osm-data.

``` bash
docker-compose run tooling ./scripts/generate-osm-data.sh /osm-data/<osm-file>
docker-compose run db ./scripts/import-osm-data.sh
```

## updating public transport stop data

Make sure that the osm-file is placed under /docker/tooling/osm-data.

``` bash
docker-compose run tooling ./scripts/generate-pt-stop-data.sh /osm-data/<osm-file>
docker-compose run db ./scripts/import-pt-stop-data.sh
```



## updating gtfs data

``` bash
docker-compose run tooling ./scripts/generate-gtfs-data.sh
docker-compose run db ./scripts/import-gtfs-data.sh
```

## updating terrain data

Make sure that the terrain-file is placed under /docker/tooling/terrain-data.

``` bash
docker-compose run tooling ./scripts/generate-terrain-data.sh /terrain-data/<terrain-file>
docker-compose run db ./scripts/import-terrain-data.sh

```