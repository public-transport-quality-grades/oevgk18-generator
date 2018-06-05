CREATE OR REPLACE FUNCTION mark_relevant_ways(distance DOUBLE PRECISION)
  RETURNS VOID AS $$
BEGIN
  UPDATE routing
    SET relevant = FALSE
  WHERE relevant IS TRUE;

  UPDATE routing
  SET relevant = TRUE FROM (
                             WITH distinct_stops AS (
                                 SELECT DISTINCT
                                   uic_ref,
                                   stop_lon,
                                   stop_lat
                                 FROM stops
                             )
                             SELECT destination.id
                             FROM
                               distinct_stops source, vertex destination
                             WHERE
                               ST_DWithin(
                                   (ST_SetSRID(ST_MakePoint(source.stop_lon, source.stop_lat), 4326)) :: geography,
                                   destination.geom_vertex :: geography,
                                   distance)
                           ) AS reachable_vertex
  WHERE routing.source = reachable_vertex.id OR routing.target = reachable_vertex.id;
END;
$$
LANGUAGE plpgsql;