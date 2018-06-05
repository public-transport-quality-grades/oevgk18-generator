CREATE OR REPLACE FUNCTION get_nearest_neighbour(stop_geom GEOMETRY)
  RETURNS RECORD AS $$
DECLARE
  ret RECORD;
BEGIN
  WITH nearest_neighbours AS (
      SELECT
        id,
        geom_vertex
      FROM vertex
      ORDER BY geom_vertex <#> stop_geom
      LIMIT 100
  )
  SELECT
        id,
        St_DistanceSphere(geom_vertex, stop_geom)
      FROM nearest_neighbours
      ORDER BY st_distance(geom_vertex, stop_geom)
      LIMIT 1
  INTO ret;
  RETURN ret;
END;
$$
LANGUAGE plpgsql;