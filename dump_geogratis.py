__author__ = 'Statistics Canada'

from ConfigParser import ConfigParser
from datetime import datetime
from db_schema import connect_to_database, Packages
import argparse


def dump_jsonl(since, dumpfile):
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')

    session = connect_to_database()
    last_id = 0

    while True:

        if args.since != '':
            package_stream = session.query(Packages).filter(Packages.id > last_id).\
                filter(Packages.updated > args.since).\
                order_by(Packages.id).limit(10).all()
        else:
            package_stream = session.query(Packages).filter(Packages.id > last_id).\
                order_by(Packages.id).limit(10).all()
        if len(package_stream) == 0:
            break
        else:
            if dumpfile != '':
                with open(dumpfile, 'a') as dfile:
                    for r in package_stream:
                        print u'Processing dataset {0}'.format(r.id)
                        dfile.write(r.ckan_json + '\n')
                        last_id = r.id
            else:
                for r in package_stream:
                    print r.ckan_json + '\n'
                    last_id = r.id

    session.close()

argparser = argparse.ArgumentParser(
    description='Scan Geogratis and save record to a database'
)
argparser.add_argument('-s', '--since', action='store', default='', dest='since',
                       help='Scan since date (e.g. 2014-01-21)')
argparser.add_argument('-f', '--file', action='store', default='', dest='dumpfile',
                       help='File to write dump to')
args = argparser.parse_args()
dumpfile = args.dumpfile
if dumpfile == '':
    dumpfile = 'geodump_{0}.jsonl'.format(datetime.now().strftime('%Y-%m-%d-%H%M%S'))
dump_jsonl(since=args.since, dumpfile=dumpfile)

