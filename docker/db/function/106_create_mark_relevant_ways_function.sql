CREATE OR REPLACE FUNCTION mark_relevant_ways(distance DOUBLE PRECISION) RETURNS VOID AS $$
BEGIN
  UPDATE routing SET relevant = TRUE FROM (
    SELECT edge
      FROM stop_vertex_mapping,
        pgr_drivingdistance('select id, source, target, km as cost from routing',
        stop_vertex_mapping.nearest_vertex_id,
        distance,
        FALSE)) AS reachable_edge
  WHERE reachable_edge.edge != -1 AND routing.id = reachable_edge.edge;
END;
$$ LANGUAGE plpgsql;
