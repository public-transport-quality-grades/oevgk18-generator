DROP TABLE IF EXISTS stop_vertex_mapping;

CREATE TABLE stop_vertex_mapping (
    id SERIAL NOT NULL PRIMARY KEY,
    stop_uic_ref BIGINT NOT NULL,
    nearest_vertex_id INTEGER NOT NULL REFERENCES vertex(id)
);

WITH neighbour AS (
	SELECT DISTINCT uic_ref, vertex_id
	FROM stops
	  CROSS JOIN LATERAL get_nearest_neighbour(ST_SetSRID(ST_MakePoint(stops.stop_lon, stops.stop_lat), 4326))
	                        AS (vertex_id INTEGER, distance DOUBLE PRECISION)
  WHERE distance < 1000
)
INSERT INTO stop_vertex_mapping (stop_uic_ref, nearest_vertex_id)
    SELECT uic_ref, vertex_id from neighbour;