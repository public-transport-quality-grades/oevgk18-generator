DROP TABLE IF EXISTS routing;

CREATE TABLE routing(id integer,
                     osm_id bigint,
                     osm_name character varying,
                     osm_meta character varying,
                     osm_source_id bigint,
                     osm_target_id bigint,
                     clazz integer,
                     flags integer,
                     source integer,
                     target integer,
                     km double precision,
                     kmh integer,
                     cost double precision,
                     reverse_cost double precision,
                     x1 double precision,
                     y1 double precision,
                     x2 double precision,
                     y2 double precision,
                     relevant bool,
                     cost_effective double precision);
SELECT AddGeometryColumn('routing', 'geom_way', 4326, 'LINESTRING', 2);
