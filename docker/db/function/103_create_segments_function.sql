CREATE OR REPLACE FUNCTION segments(gid_input INTEGER, segment_length INTEGER DEFAULT 100) RETURNS TABLE(geom geometry) AS $$
BEGIN
   RETURN QUERY
   SELECT ST_LineSubstring(the_geom, segment_length*n/length,
       CASE
          WHEN segment_length*(n+1) < length THEN segment_length*(n+1)/length
          ELSE 1
       END
   ) As new_geom
   FROM
      (SELECT ST_LineMerge(routing.geom_way) AS the_geom, cost As length FROM routing where routing.id = gid_input) AS t
          CROSS JOIN generate_series(0,10000) AS n WHERE n*segment_length/length < 1;
END;
$$ LANGUAGE plpgsql