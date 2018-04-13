CREATE TABLE agency
(
  agency_id         text UNIQUE NULL,
  agency_name       text NOT NULL,
  agency_url        text NOT NULL,
  agency_timezone   text NOT NULL,
  agency_lang       text NULL,
  agency_phone      text NULL
);

CREATE TABLE stops
(
  stop_id           text PRIMARY KEY,
  stop_code         text NULL,
  stop_name         text NOT NULL,
  stop_desc         text NULL,
  stop_lat          double precision NOT NULL,
  stop_lon          double precision NOT NULL,
  stop_elevation    integer NULL,
  zone_id           text NULL,
  stop_url          text NULL,
  location_type     boolean NULL,
  parent_station    text NULL,
  platform_code     text NULL,
  ch_station_long_name  text NULL,
  ch_station_synonym1   text NULL,
  ch_station_synonym2   text NULL,
  ch_station_synonym3   text NULL,
  ch_station_synonym4   text NULL
);

CREATE TABLE routes
(
  route_id          text PRIMARY KEY,
  agency_id         text NULL references agency(agency_id),
  route_short_name  text NULL,
  route_long_name   text NULL,
  route_desc        text NULL,
  route_type        integer NULL,
  route_url         text NULL,
  route_color       text NULL,
  route_text_color  text NULL
);

CREATE TABLE calendar
(
  service_id        text PRIMARY KEY,
  monday            boolean NOT NULL,
  tuesday           boolean NOT NULL,
  wednesday         boolean NOT NULL,
  thursday          boolean NOT NULL,
  friday            boolean NOT NULL,
  saturday          boolean NOT NULL,
  sunday            boolean NOT NULL,
  start_date        numeric(8) NOT NULL,
  end_date          numeric(8) NOT NULL
);

CREATE TABLE calendar_dates
(
  service_id text NOT NULL,
  date numeric(8) NOT NULL,
  exception_type integer NOT NULL
);


CREATE TABLE trips
(
  route_id          text NOT NULL references routes(route_id),
  service_id        text NOT NULL, -- TODO: referential integrity to both calendar and calendar_dates
  trip_id           text NOT NULL PRIMARY KEY,
  trip_headsign     text NULL,
  trip_short_name   text NULL,
  direction_id      boolean NULL,
  block_id          text NULL,
  shape_id          text NULL,
  bikes_allowed     integer NULL,
  attributes_ch     text NULL
);

CREATE TABLE stop_times
(
  trip_id           text NOT NULL references trips(trip_id),
  arrival_time      interval NULL, -- should be not null according to spec
  departure_time    interval NULL, -- should be not null according to spec
  stop_id           text NOT NULL references stops(stop_id),
  stop_sequence     integer NOT NULL,
  stop_headsign     text NULL,
  pickup_type       integer NULL CHECK(pickup_type >= 0 and pickup_type <=3),
  drop_off_type     integer NULL CHECK(drop_off_type >= 0 and drop_off_type <=3),
  shape_dist_traveled integer NULL,
  attributes_ch     text NULL
);

CREATE TABLE transfers
(
    from_stop_id  text NOT NULL references stops(stop_id),
    to_stop_id    text NOT NULL references stops(stop_id),
    transfer_type   integer NOT NULL,
    min_transfer_time integer
);

CREATE TABLE frequencies
(
    trip_id       text NOT NULL references trips(trip_id),
    start_time    interval NOT NULL,
    end_time      interval NOT NULL,
    headway_secs  integer NOT NULL
);