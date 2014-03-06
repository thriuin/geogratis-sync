geogratis-sync
==============

Python utility application to keep in sync with NRCAN's Geogratis service

Database Scripts
----------------

Use the following SQL script to create the table that holds the results of the Geogratis scan::

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
        json_record_fr TEXT,
        od_updated TIMESTAMP WITHOUT TIME ZONE
    );


*temp* alter table geogratis_records add column od_updated timestamp without time zone,
                                     add column od_status TEXT;