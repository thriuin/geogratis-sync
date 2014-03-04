geogratis-sync
==============

Python utility application to keep in sync with NRCAN's Geogratis service

Database Scripts
----------------

CREATE TABLE geogratis_records (
    id serial PRIMARY KEY NOT NULL,
    uuid TEXT,
    title_en TEXT,
    title_fr TEXT,
    created TIMESTAMP WITHOUT TIME ZONE,
    updated TIMESTAMP WITHOUT TIME ZONE,
    edited TIMESTAMP WITHOUT TIME ZONE,
    state TEXT,
    json_record_en TEXT,
    json_record_fr TEXT
);
