__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import argparse
from db_schema import connect_to_database, find_all_geogratis_records

argparser = argparse.ArgumentParser(description='Scan Geogratis and save record to a database')
argparser.add_argument('-o', '--outfile',
                       action='store',
                       default='geogratis_update.jsonl',
                       dest='outfile',
                       help='Write extracted CKAN JSONL to this file')
args = argparser.parse_args()

session = connect_to_database()
known_records = find_all_geogratis_records(session)
jfile = open(args.outfile, mode='w')
for r in known_records:
    if r.od_status == 'Needs Update' or r.od_status == 'New Record' and r.ckan_json is not None:
        print >> jfile, r.ckan_json
jfile.close()
