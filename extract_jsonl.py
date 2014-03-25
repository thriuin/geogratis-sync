__author__ = 'thomros'

from db_schema import connect_to_database, find_all_geogratis_records

session = connect_to_database()
known_records = find_all_geogratis_records(session)
jfile = open('geo.jsonl', mode='w')
for r in known_records:
    print >> jfile, r.ckan_json
jfile.close()
