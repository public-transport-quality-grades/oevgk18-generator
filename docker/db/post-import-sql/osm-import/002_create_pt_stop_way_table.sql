DROP TABLE IF EXISTS pt_stop_way;

CREATE TABLE pt_stop_way (
    id SERIAL NOT NULL PRIMARY KEY,
    pt_stop_id BIGINT NOT NULL REFERENCES pt_stop(id),
    entry_way_id INTEGER NOT NULL REFERENCES routing(id)
);

INSERT INTO pt_stop_way (pt_stop_id, entry_way_id) SELECT pt_stop.id, min_distance(pt_stop.geom) from pt_stop;