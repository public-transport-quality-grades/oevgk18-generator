TRUNCATE intercity_stations;
COPY intercity_stations FROM '/post-import-sql/intercity_railway_stations.csv' WITH (
FORMAT csv, HEADER TRUE
);