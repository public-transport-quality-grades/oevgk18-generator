CREATE OR REPLACE FUNCTION segments(geom_way GEOMETRY, length_m DOUBLE PRECISION, segment_length INTEGER DEFAULT 100)
  RETURNS TABLE(geom geometry) AS $$
BEGIN
  IF length_m = 0.0
  THEN
    RETURN QUERY SELECT ST_GeomFromText('LINESTRING EMPTY');
  ELSE
    RETURN QUERY
    SELECT ST_LineSubstring(ST_LineMerge(geom_way), segment_length * n / length_m,
                            CASE
                            WHEN segment_length * (n + 1) < length_m
                              THEN segment_length * (n + 1) / length_m
                            ELSE 1
                            END
           ) As new_geom
    FROM generate_series(0, 10000) AS n
    WHERE n * segment_length / length_m < 1;
  END IF;
END;
$$
LANGUAGE plpgsql;