CREATE INDEX ON stops(stop_id);
CREATE INDEX ON stop_times(stop_id);
CREATE INDEX ON stop_times(trip_id);
CREATE INDEX ON trips(trip_id);
CREATE INDEX ON trips(route_id);
CREATE INDEX ON routes(route_id);

DROP TABLE IF EXISTS next_station_mapping;
CREATE TABLE next_station_mapping AS
	SELECT DISTINCT s.stop_name, t.trip_id, st.stop_sequence, s.parent_station FROM stops s
		INNER JOIN stop_times st ON s.stop_id = st.stop_id
		INNER JOIN trips t ON st.trip_id = t.trip_id
		INNER JOIN routes r ON t.route_id = r.route_id
	WHERE r.route_type = 2 OR r.route_type = 1;

CREATE INDEX ON next_station_mapping(trip_id);
CREATE INDEX ON next_station_mapping(parent_station);
CREATE INDEX ON next_station_mapping(stop_name);