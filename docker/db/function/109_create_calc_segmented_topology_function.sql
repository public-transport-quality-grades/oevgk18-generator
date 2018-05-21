CREATE OR REPLACE FUNCTION calc_segmented_topology(partition_size INTEGER) RETURNS VOID AS $$
DECLARE
  min_id INTEGER;
  max_id INTEGER;
  counter_min INTEGER;
  counter_max INTEGER;
BEGIN
 SELECT min(id) INTO min_id FROM routing_segmented;
 SELECT max(id) INTO max_id FROM routing_segmented;
 counter_min := min_id;

 DROP TABLE IF EXISTS routing_segmented_vertices_pgr;

 WHILE counter_min <= max_id LOOP
  counter_max := counter_min + (max_id - min_id) / partition_size;
  RAISE NOTICE 'Create topology for IDs % to %', counter_min, counter_max;
  PERFORM pgr_createTopology(
      'routing_segmented', 0.00001, 'geom_way', 'id', rows_where:='id >= ' || counter_min || ' AND id < ' || counter_max);
  counter_min := counter_max;
 END LOOP;

END;
$$ LANGUAGE plpgsql;