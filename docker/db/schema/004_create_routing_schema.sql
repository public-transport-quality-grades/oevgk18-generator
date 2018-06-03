DROP TABLE IF EXISTS routing;

CREATE TABLE routing (
  id            INTEGER,
  osm_id        BIGINT,
  osm_name      character varying,
  osm_meta      character varying,
  osm_source_id BIGINT,
  osm_target_id BIGINT,
  clazz         INTEGER,
  flags         INTEGER,
  source        INTEGER,
  target        INTEGER,
  km            DOUBLE PRECISION,
  kmh           INTEGER,
  cost          DOUBLE PRECISION,
  reverse_cost  DOUBLE PRECISION,
  x1            DOUBLE PRECISION,
  y1            DOUBLE PRECISION,
  x2            DOUBLE PRECISION,
  y2            DOUBLE PRECISION,
  relevant      BOOLEAN
);
SELECT AddGeometryColumn('routing', 'geom_way', 4326, 'LINESTRING', 2);

DROP TABLE IF EXISTS routing_segmented;
CREATE TABLE routing_segmented (
  id             SERIAL,
  osm_id         INTEGER,
  source         INTEGER,
  target         INTEGER,
  cost           DOUBLE PRECISION,
  cost_effective DOUBLE PRECISION
);
SELECT AddGeometryColumn('routing_segmented', 'geom_way', 4326, 'LINESTRING', 2);
