__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import argparse
from db_schema import connect_to_database, find_all_records, Packages

argparser = argparse.ArgumentParser(description='Ext')
argparser.add_argument('-o', '--outfile',
                       action='store',
                       default='geogratis_update.jsonl',
                       dest='outfile',
                       help='Write extracted CKAN JSONL to this file')
argparser.add_argument('-m', '--maxrecords',
                       action='store',
                       default=0,
                       type=int,
                       dest='maxrecords',
                       help='Maximum number of records to retrieve. 0 means retrieve all')
argparser.add_argument('-n', '--newonly',
                       action='store_true',
                       dest='newonly',
                       default=False,
                       help='Only extract new records')
args = argparser.parse_args()

session = connect_to_database()
last_id = 0
jfile = open(args.outfile, mode='w')
rec_count = 1
while True:
    known_records = find_all_records(session, query_class=Packages, query_limit=10, limit_id=last_id)
    if len(known_records) == 0:
        break
    else:
        for r in known_records:
            if args.newonly and r.status == 'update':
                continue
            if (r.status == 'new' or r.status == 'update') and r.package is not None:
                print >> jfile, r.package
                rec_count += 1
                if 0 < args.maxrecords < rec_count:
                    break
    if 0 < args.maxrecords < rec_count:
        break

    last_id = r.id
print "{0} Records Exported".format(rec_count - 1)
jfile.close()
