# oevgk18-generator docker

## start database

``` bash
docker-compose up -d
```

## updating osm data

Make sure that the osm-file is placed under `docker/tooling/osm-data`

``` bash
docker-compose run tooling generate-osm-data.sh /osm-data/<osm-file>
docker-compose run db import-osm-data.sh
```

## updating public transport stop data

Make sure that the osm-file is placed under `docker/tooling/osm-data`.

``` bash
docker-compose run tooling generate-pt-stop-data.sh /osm-data/<osm-file>
docker-compose run db import-pt-stop-data.sh
```



## updating gtfs data

``` bash
docker-compose run tooling generate-gtfs-data.sh
docker-compose run db import-gtfs-data.sh
```

## updating terrain data

Make sure that the terrain-file is placed under `docker/tooling/terrain-data`.

``` bash
docker-compose run tooling generate-terrain-data.sh /terrain-data/<terrain-file>
docker-compose run db import-terrain-data.sh

```