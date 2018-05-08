CREATE OR REPLACE FUNCTION isochrones(start_vertex INTEGER, boundaries NUMERIC[])
  RETURNS TABLE(distance NUMERIC, polygon GEOMETRY) AS $$
BEGIN
  CREATE TEMP TABLE distances ON COMMIT DROP AS (
	  SELECT id, boundary AS distance, geom_vertex as point
			FROM unnest(boundaries) boundary,
			LATERAL pgr_drivingDistance(
          'SELECT id, source, target, cost_effective AS cost FROM routing WHERE relevant IS TRUE',
          start_vertex,
          boundary,
          FALSE
			) AS isochron INNER JOIN vertex ON isochron.node = vertex.id
	);

  RETURN QUERY
    WITH relevant_bounderies as (
      SELECT boundary FROM unnest(boundaries) boundary, distances d WHERE d.distance = boundary GROUP BY boundary HAVING count(d.distance) >= 3
    )
    SELECT boundary, polygon_geom as polygon
      FROM relevant_bounderies,
      LATERAL pgr_pointsAsPolygon(
          'SELECT id::integer, ST_X(point)::float AS x, ST_Y(point)::float AS y FROM distances WHERE distance <= ' || boundary || ';'
      ) AS polygon_geom WHERE polygon_geom IS NOT NULL;
  END;
$$ LANGUAGE plpgsql