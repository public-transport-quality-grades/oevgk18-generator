DROP TABLE IF EXISTS pt_stop_way;

CREATE TABLE pt_stop_way (
    id SERIAL NOT NULL PRIMARY KEY,
    pt_stop_id BIGINT NOT NULL,
    entry_way_id INTEGER NOT NULL REFERENCES routing(id)
);

INSERT INTO pt_stop_way (pt_stop_id, entry_way_id)
    SELECT DISTINCT  uic_ref, get_source(ST_SetSRID(ST_MakePoint(stop_lon, stop_lat),4326))
    FROM stops;