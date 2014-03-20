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
        geogratis_scanned TIMESTAMP WITHOUT TIME ZONE,
        last_comparison TIMESTAMP WITHOUT TIME ZONE,
        od_updated TIMESTAMP WITHOUT TIME ZONE,
        od_status TEXT,
        differences TEXT,
        ckan_json TEXT
    );


Open Data Meta Data Model
-------------------------

Geogratis and Open Data/CKAN have slightly different metadata models for data sets. When considering
whether or not the Open Data record is different from the Geogratis records, only a subset of fields are
compared.


+----------------------------------+--------------------------------------+
| Dataset Metadata                                                        |
+==================================+======================================+
| CKAN                             | Geogratis                            |
+==================================+======================================+
| url                              | N/A (Calculated field)               |
+----------------------------------+--------------------------------------+
| url_fra                          | N/A (Calculated field)               |
+----------------------------------+--------------------------------------+
| title                            | title (EN - English record)          |
+----------------------------------+--------------------------------------+
| title_fra                        | title (FR - French record)           |
+----------------------------------+--------------------------------------+
| notes                            | summary (EN)                         |
+----------------------------------+--------------------------------------+
| notes_fra                        | summary (FR)                         |
+----------------------------------+--------------------------------------+
| date_modified                    | updatedDate                          |
+----------------------------------+--------------------------------------+
| data_series_name                 | citation.series (EN)                 |
+----------------------------------+--------------------------------------+
| data_series_name_fra             | citation.series (FR)                 |
+----------------------------------+--------------------------------------+
| keywords (list)                  | keywords (EN)                        |
+----------------------------------+--------------------------------------+
| keywords_fra (list)              | keywords (FR)                        |
+----------------------------------+--------------------------------------+
| spatial                          | geometry (calculated)                |
+----------------------------------+--------------------------------------+
| presentation_form                | citation.presentationForm            |
+----------------------------------+--------------------------------------+
| digital_object_identifier        | citation.otherCitationDetails        |
+----------------------------------+--------------------------------------+
| geographic_region                | categories.urn:iso:place(calculated) |
+----------------------------------+--------------------------------------+
| data_series_issue_identification | citation.seriesIndex                 |
+----------------------------------+--------------------------------------+
| presentation_form                | citation.prsentationForm             |
+----------------------------------+--------------------------------------+
| browse_graphic_url               | browseImages[0]                      |
+----------------------------------+--------------------------------------+
| topic_category (list)            | topicCategories (list)               |
+----------------------------------+--------------------------------------+
| state                            | deleted                              |
+----------------------------------+--------------------------------------+


+----------------------------------+--------------------------------------+
| Resource Metadata (list)                                                |
+==================================+======================================+
| CKAN                             | Geogratis                            |
+==================================+======================================+
| name                             | files[].description (EN)             |
+----------------------------------+--------------------------------------+
| name_fra                         | files[].description (FR)             |
+----------------------------------+--------------------------------------+
| url                              | files[].link                         |
+----------------------------------+--------------------------------------+
| format                           | files[].type                         |
+----------------------------------+--------------------------------------+

