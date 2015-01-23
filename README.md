# geogratis-sync

Python utility application to keep in sync with NRCAN's Geogratis service

## Open Data Meta Data Model

Geogratis and Open Data/CKAN have slightly different metadata models for data sets. When considering
whether or not the Open Data record is different from the Geogratis records, only a subset of fields are
compared.


### Dataset Metadata

This table indicates how CKAN dataset metadata fields are mapped to Geogratris metadata fields

 CKAN                             | Geogratis                            
 -------------------------------- | ------------------------------------ 
 url                              | N/A (Calculated field)               
 url_fra                          | N/A (Calculated field)               
 title                            | title (EN - English record)          
 title_fra                        | title (FR - French record)           
 notes                            | summary (EN)                         
 notes_fra                        | summary (FR)                         
 date_modified                    | updatedDate                          
 data_series_name                 | citation.series (EN)                 
 data_series_name_fra             | citation.series (FR)                 
 keywords (list)                  | keywords (EN)                        
 keywords_fra (list)              | keywords (FR)                        
 spatial                          | geometry (calculated)                
 presentation_form                | citation.presentationForm            
 digital_object_identifier        | citation.otherCitationDetails        
 geographic_region                | categories.urn:iso:place(calculated) 
 data_series_issue_identification | citation.seriesIndex                 
 presentation_form                | citation.prsentationForm             
 browse_graphic_url               | browseImages                 
 topic_category (list)            | topicCategories (list)               
 state                            | deleted                              


### Resource Metadata (list)

This table indicates how CKAN resource metadata fields are mapped to Geogratris metadata fields

 CKAN                             | Geogratis                           
 -------------------------------- | ------------------------------------ 
 name                             | files[].description (EN)            
 name_fra                         | files[].description (FR)            
 url                              | files[].link                        
 format                           | files[].type                        


## Scanning Geogratis

### Getting Started

The Geogratis Scanner for Open Data is a Python application, and makes use of a small number of Python libraries.
Assuming you are using virtualenv and pip (or equivalent), the required libraries are enumerated in the requirements.txt
file. To install the required libraries using pip:

```pip install -r requirements.txt```

For more information on how to use virtualenv and pip see:

* [Virtualenv](http://virtualenv.readthedocs.org/en/latest/)
* [Pip](http://pip.readthedocs.org/en/latest/user_guide.html)



### Database Scripts

Meant for use, CKAN, the Geogratis scanner saves data to a PostgreSQL database. 
Use the following SQL script to create the table that holds the results of the Geogratis scan

    ```sql
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
        od_status TEXT
    );
    
    CREATE TABLE package_updates (
        id serial PRIMARY KEY NOT NULL,
        uuid TEXT,
        created TIMESTAMP WITHOUT TIME ZONE,
        updated TIMESTAMP WITHOUT TIME ZONE,
        ckan_json TEXT,
        message TEXT DEFAULT ''
    );
    
    CREATE TABLE settings (
        id serial PRIMARY KEY NOT NULL,    
        setting_name TEXT NOT NULL,
        setting_value TEXT DEFAULT ''
    );
    ```

The Geogratis scanner will need read/write access to these three tables.

### geogratis.ini file

The scanner needs a number of runtime parameters such as database connection information. Set the
following values in this .ini.

```
 [sqlalchemy]
 # This is the SQLAlchemy database connection string to the PostgreSQL database
 sqlalchemy.url = postgresql://dbuser:password@hostname/database
```

## Scanning Geogratis

Scanning Geogratis, or other data sources, is a 3 step process

1. Harvest the data from the source and save it into a records table (geogratis_records)
2. Convert the harvested data into the internal format used by CKAN. 
   The CKAN dataset json is generated and saved to the package_updates table.
3. Update CKAN based on the updates stored in the package_updates table. 
