DROP TABLE IF EXISTS stop_vertex_mapping;

CREATE TABLE stop_vertex_mapping (
    id SERIAL NOT NULL PRIMARY KEY,
    stop_uic_ref BIGINT NOT NULL,
    nearest_vertex_id INTEGER NOT NULL REFERENCES vertex(id)
);

INSERT INTO stop_vertex_mapping (stop_uic_ref, nearest_vertex_id)
    SELECT DISTINCT uic_ref, get_nearest_neighbour(ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326)) FROM stops;