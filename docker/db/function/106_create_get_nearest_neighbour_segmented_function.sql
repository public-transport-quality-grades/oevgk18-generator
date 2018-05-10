CREATE OR REPLACE FUNCTION get_nearest_neighbour_segmented(stop_geom GEOMETRY) RETURNS RECORD AS $$
DECLARE
  ret RECORD;
BEGIN
  SELECT id, St_DistanceSphere(the_geom, stop_geom)
  FROM routing_segmented_vertices_pgr
    ORDER BY the_geom <#> stop_geom
    LIMIT 1 into ret;
   RETURN ret;
END;
$$ LANGUAGE plpgsql;