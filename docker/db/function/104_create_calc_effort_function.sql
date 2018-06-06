CREATE OR REPLACE FUNCTION calc_effective_effort(distance DOUBLE PRECISION,
                                                 incline_metres_in_altitude DOUBLE PRECISION,
                                                 decline_metres_in_altitude DOUBLE PRECISION,
                                                 decline INTEGER)
  RETURNS DOUBLE PRECISION AS $$
DECLARE
  effort  DOUBLE PRECISION := 0.0;
BEGIN
  effort := distance + (incline_metres_in_altitude / 100) * 1000;
  IF decline != 0 AND decline_metres_in_altitude / decline > 0.2
  THEN
    effort := effort + (decline_metres_in_altitude / 150) * 1000;
  END IF;
  RETURN effort;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_effort(gid_input INTEGER)
  RETURNS RECORD AS $$
DECLARE
  segment                    RECORD;
  segment_length             INTEGER := 10;
  distance                   DOUBLE PRECISION;
  incline                    INTEGER := 0;
  decline                    INTEGER := 0;
  incline_metres_in_altitude DOUBLE PRECISION := 0.0;
  decline_metres_in_altitude DOUBLE PRECISION := 0.0;
  effort                     DOUBLE PRECISION := 0.0;
  reverse_effort             DOUBLE PRECISION := 0.0;
  ret                        RECORD;
BEGIN
  FOR segment IN
  SELECT
    get_height(transform_to_2056(st_startpoint(seg.geom))) AS start,
    get_height(transform_to_2056(st_endpoint(seg.geom)))   AS destination
  FROM routing_segmented AS r
    CROSS JOIN segments(r.geom_way, r.cost, segment_length) AS seg
  WHERE r.id = gid_input
  LOOP
    IF segment.start < segment.destination
    THEN
      incline := incline + segment_length;
      incline_metres_in_altitude := incline_metres_in_altitude + (segment.destination - segment.start);
    ELSEIF segment.start > segment.destination
      THEN
        decline := decline + segment_length;
        decline_metres_in_altitude := decline_metres_in_altitude + segment.start - segment.destination;
    END IF;
  END LOOP;

  SELECT cost
  INTO distance
  FROM routing_segmented
  WHERE id = gid_input;

  SELECT calc_effective_effort(distance,
                               incline_metres_in_altitude,
                               decline_metres_in_altitude,
                               decline)
  INTO effort;

  SELECT calc_effective_effort(distance,
                               decline_metres_in_altitude,
                               incline_metres_in_altitude,
                               incline)
  INTO reverse_effort;

  SELECT effort, reverse_effort INTO ret;
  RETURN ret;
END;
$$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION calc_effort(start_id INTEGER, end_id INTEGER)
  RETURNS VOID AS $$
BEGIN
  UPDATE routing_segmented
  SET (effort, reverse_effort) =
    (SELECT effort, reverse_effort FROM get_effort(id) AS (effort DOUBLE PRECISION, reverse_effort DOUBLE PRECISION))
  WHERE id >= start_id AND id <= end_id;
END;
$$
LANGUAGE plpgsql;


