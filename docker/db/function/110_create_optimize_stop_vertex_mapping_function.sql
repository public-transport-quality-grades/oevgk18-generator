CREATE OR REPLACE FUNCTION optimize_stop_vertex_mapping() RETURNS VOID AS $$
BEGIN
 TRUNCATE stop_vertex_mapping;

WITH neighbour AS (
	SELECT DISTINCT uic_ref, vertex_id
	FROM stops
	  CROSS JOIN LATERAL get_nearest_neighbour_segmented(ST_SetSRID(ST_MakePoint(stops.stop_lon, stops.stop_lat), 4326))
	                        AS (vertex_id BIGINT, distance DOUBLE PRECISION)
  WHERE distance < 300
)
INSERT INTO stop_vertex_mapping (stop_uic_ref, nearest_vertex_id)
    SELECT uic_ref, vertex_id from neighbour;
END;
$$ LANGUAGE plpgsql;
