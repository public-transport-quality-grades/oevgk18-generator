CREATE TABLE person (
     id    integer,
     name   varchar(40) NOT NULL CHECK (name <> '')
);

INSERT INTO person VALUES (1, 'Muster');