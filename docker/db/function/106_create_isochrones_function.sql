CREATE OR REPLACE FUNCTION isochrones(start_vertex INTEGER, boundaries NUMERIC [])
  RETURNS TABLE(distance NUMERIC, polygon GEOMETRY) AS $$
DECLARE
  start_vertex_geom GEOMETRY;
  max_boundary      NUMERIC;
BEGIN
  SELECT the_geom
  INTO start_vertex_geom
  FROM routing_segmented_vertices_pgr
  WHERE id = start_vertex;

  SELECT max(boundary)
  INTO max_boundary
  FROM unnest(boundaries) boundary;

  CREATE TEMP TABLE edge_preselection ON COMMIT DROP AS (
    SELECT
      id,
      source,
      target,
      effort AS reverse_cost, -- reverse directionality to simulate walking towards the public transport stop
      reverse_effort as cost
    FROM routing_segmented r
    -- select edges within ~1200 meters from the start vertex
    WHERE ST_intersects(ST_Buffer(start_vertex_geom, 0.013), r.geom_way)
  );

  CREATE TEMP TABLE distances ON COMMIT DROP AS (
    SELECT
      vertices.id,
      vertices.the_geom AS point,
      isochron.agg_cost as distance
    FROM pgr_drivingDistance(
             'SELECT id, source, target, cost, reverse_cost FROM edge_preselection',
             start_vertex,
             max_boundary,
             TRUE
         ) AS isochron
      INNER JOIN routing_segmented_vertices_pgr vertices ON isochron.node = vertices.id
  );

  RETURN QUERY
  WITH relevant_bounderies AS (
      SELECT boundary
      FROM unnest(boundaries) boundary, distances d
      WHERE d.distance <= boundary
      GROUP BY boundary
      HAVING count(d.distance) >= 3
  )
  SELECT
    boundary,
    polygon_geom AS polygon
  FROM relevant_bounderies,
      LATERAL st_buffer(
          pgr_pointsAsPolygon(
              'SELECT id::integer, ST_X(point)::float AS x, ST_Y(point)::float AS y FROM distances WHERE distance <= '
              || boundary || ';',
              0.00005
          ), 0.0001) AS polygon_geom
  WHERE polygon_geom IS NOT NULL;
END;
$$
LANGUAGE plpgsql