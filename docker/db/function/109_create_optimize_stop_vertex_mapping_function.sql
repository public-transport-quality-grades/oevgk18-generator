CREATE OR REPLACE FUNCTION optimize_stop_vertex_mapping()
  RETURNS VOID AS $$
BEGIN

  TRUNCATE stop_vertex_mapping;


  WITH unique_stops AS (
      SELECT DISTINCT
        uic_ref,
        stop_lon,
        stop_lat
      FROM stops
      WHERE uic_ref > 8500000
  ),
  neighbour AS (
      SELECT
        uic_ref,
        get_nearest_neighbour_segmented(stop_lon, stop_lat) AS vertex_id
      FROM unique_stops
  )
  INSERT INTO stop_vertex_mapping (stop_uic_ref, nearest_vertex_id)
      SELECT
        uic_ref,
        vertex_id
      FROM neighbour
      WHERE vertex_id IS NOT NULL;
END;
$$
LANGUAGE plpgsql;
