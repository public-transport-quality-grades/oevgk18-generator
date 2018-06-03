CREATE OR REPLACE FUNCTION get_nearest_neighbour(stop_geom GEOMETRY)
  RETURNS RECORD AS $$
DECLARE
  ret RECORD;
BEGIN
  SELECT
    id,
    St_DistanceSphere(geom_vertex, stop_geom)
  FROM vertex
  ORDER BY geom_vertex <#> stop_geom
  LIMIT 1
  INTO ret;
  RETURN ret;
END;
$$
LANGUAGE plpgsql;