CREATE OR REPLACE FUNCTION mark_relevant_ways() RETURNS VOID AS $$
BEGIN
  UPDATE routing SET relevant = TRUE FROM (
    SELECT edge
      FROM pt_stop_way,
        pgr_drivingdistance('select id, source, target, km as cost from routing',
        pt_stop_way.entry_way_id,
        0.300)) as reachable_edge
  WHERE routing.id = reachable_edge.edge;
END;
$$ LANGUAGE plpgsql;
