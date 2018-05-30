CREATE OR REPLACE FUNCTION get_nearest_neighbour_segmented(stop_lon DOUBLE PRECISION, stop_lat double precision)
  RETURNS BIGINT AS $$
DECLARE
  nearest_vertex BIGINT;
  max_distance INTEGER;
  count_intersects INTEGER;
BEGIN
  TRUNCATE edge_preselection;

  INSERT INTO edge_preselection
    SELECT id, source, target, cost
    FROM routing_segmented r
    WHERE ST_contains(ST_Buffer(ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326), 0.013), r.geom_way);

   SELECT COUNT(*)
    INTO count_intersects
    FROM edge_preselection;
  IF count_intersects < 1 THEN
    RAISE NOTICE 'Stop %, % is outside boundaries', stop_lon, stop_lat;
    RETURN NULL;
  END IF;
  FOR nearest_vertex IN
  SELECT id
    FROM routing_segmented_vertices_pgr v
    ORDER BY v.the_geom <#> ST_SetSRID(ST_MakePoint(stop_lon, stop_lat), 4326)
    LIMIT 100
  LOOP

   SELECT max(agg_cost) INTO max_distance FROM pgr_drivingDistance(
          'SELECT id, source, target, cost FROM edge_preselection',
          nearest_vertex,
          200,
          FALSE);

  IF max_distance >= 150 THEN
    RETURN nearest_vertex;
  END IF;
      RAISE NOTICE '%, %: vertex % has a reachable distance of %', stop_lat, stop_lon, nearest_vertex, max_distance;
  END LOOP;
      RAISE NOTICE 'no good snapping found for %, %', stop_lat, stop_lon;
      RETURN NULL;
END;
$$ LANGUAGE plpgsql;