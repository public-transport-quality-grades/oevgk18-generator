CREATE OR REPLACE FUNCTION segment_routing_graph(segment_size_m INTEGER)
  RETURNS VOID AS $$
BEGIN
  DROP TABLE IF EXISTS routing_segmented_vertices_pgr;
  TRUNCATE routing_segmented;
  INSERT INTO routing_segmented (geom_way, osm_id)
    SELECT
      segs.geom,
      routing.osm_id
    FROM routing
      CROSS JOIN segments(routing.geom_way, routing.km * 1000, segment_size_m) AS segs
    WHERE routing.relevant IS TRUE AND routing.km != 0;
END;
$$
LANGUAGE plpgsql;