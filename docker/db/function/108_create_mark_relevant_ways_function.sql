CREATE OR REPLACE FUNCTION mark_relevant_ways(distance DOUBLE PRECISION)
  RETURNS VOID AS $$
BEGIN
  UPDATE routing
  SET relevant = TRUE FROM (SELECT destination.id
                            FROM
                              stop_vertex_mapping svm LEFT JOIN vertex source ON svm.nearest_vertex_id = source.id
                              , vertex destination
                            WHERE ST_DWithin(source.geom_vertex :: geography, destination.geom_vertex :: geography,
                                             distance)
                           ) AS reachable_vertex
  WHERE routing.source = reachable_vertex.id OR routing.target = reachable_vertex.id;
END;
$$
LANGUAGE plpgsql;