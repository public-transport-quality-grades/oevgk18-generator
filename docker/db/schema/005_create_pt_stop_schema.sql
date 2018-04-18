DROP TABLE IF EXISTS pt_stop;

-- Create a table for pt_stop.
CREATE TABLE pt_stop (
    id bigint NOT NULL,
    version int NOT NULL,
    user_id int NOT NULL,
    tstamp timestamp without time zone NOT NULL,
    changeset_id bigint NOT NULL,
    tags hstore
);
-- Add a postgis point column holding the location of the pt_stop.
SELECT AddGeometryColumn('pt_stop', 'geom', 4326, 'POINT', 2);

-- Add primary keys to tables.
ALTER TABLE ONLY pt_stop ADD CONSTRAINT pk_pt_stop PRIMARY KEY (id);

-- Add indexes to tables.
CREATE INDEX idx_pt_stop_geom ON pt_stop USING gist (geom);

-- Set to cluster pt_stop by geographical location.
ALTER TABLE ONLY pt_stop CLUSTER ON idx_pt_stop_geom;