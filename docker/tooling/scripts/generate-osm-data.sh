#!/bin/sh

java -jar osm2po-core-5.2.43-signed.jar cmd=tjspg $1
mv /osm/osm_2po_4pgr.sql /sql-import/import-osm-data.sql