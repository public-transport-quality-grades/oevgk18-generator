#!/bin/sh

java -jar /opt/osm2po/osm2po-core-5.2.43-signed.jar cmd=tjspg $1

sed -i 's/osm_2po_4pgr/routing/g' /osm/osm_2po_4pgr.sql
mv /osm/osm_2po_4pgr.sql /sql-import/import-osm-data.sql

sed -i 's/osm_2po_vertex/vertex/g' /osm/osm_2po_vertex.sql
cat /osm/osm_2po_vertex.sql >> /sql-import/import-osm-data.sql
