__author__ = 'Statistics Canada'

from ConfigParser import ConfigParser
from datetime import datetime
from db_schema import connect_to_database, Packages, get_setting
from sys import stderr
import argparse


argparser = argparse.ArgumentParser(
    description='Scan Geogratis and save record to a database'
)
argparser.add_argument('-s', '--since', action='store', default='', dest='since',
                       help='Scan since date (e.g. 2014-01-21)')
argparser.add_argument('-f', '--file', action='store', default='', dest='dumpfile',
                       help='File to write dump to')
argparser.add_argument('-m', '--monitor', action='store_true', default=False, dest='monitor')
argparser.add_argument('-n', '--new-only', action='store_true', default=False, dest='new_only',
                       help='Only dump files that do not already have records in the OD portal')
argparser.add_argument('-u', '--update-only', action='store_true', default=False, dest='update_only',
                       help='Only dump files that do already have records in the OD portal. Cannot be used with the \
new-only option')
args = argparser.parse_args()


def main(since, dumpfile):
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')

    session = connect_to_database()
    last_id = 0

    while True:
        # @todo clean - up the messy if statement here
        if args.monitor:
            last_run_setting = get_setting('last_conversion_run')
            if last_run_setting.setting_value:
                if args.new_only:
                    package_stream = session.query(Packages).filter(Packages.id > last_id).\
                        filter(Packages.updated > last_run_setting.setting_value).\
                        filter(not Packages.existing).\
                        order_by(Packages.id).limit(10).all()
                elif args.update_only:
                    package_stream = session.query(Packages).filter(Packages.id > last_id).\
                        filter(Packages.updated > last_run_setting.setting_value).\
                        filter(Packages.existing).\
                        order_by(Packages.id).limit(10).all()
                else:
                    package_stream = session.query(Packages).filter(Packages.id > last_id).\
                        filter(Packages.updated > last_run_setting.setting_value).\
                        order_by(Packages.id).limit(10).all()
            else:
                if args.new_only:
                    package_stream = session.query(Packages).filter(Packages.id > last_id). \
                        filter(not Packages.existing).\
                        order_by(Packages.id).limit(10).all()
                elif args.update_only:
                    package_stream = session.query(Packages).filter(Packages.id > last_id). \
                        filter(Packages.existing).\
                        order_by(Packages.id).limit(10).all()
                else:
                    package_stream = session.query(Packages).filter(Packages.id > last_id).\
                        order_by(Packages.id).limit(10).all()
        elif args.since != '':
            if args.new_only:
                package_stream = session.query(Packages).filter(Packages.id > last_id).\
                    filter(Packages.updated > args.since). \
                    filter(not Packages.existing).\
                    order_by(Packages.id).limit(10).all()
            elif args.update_only:
                package_stream = session.query(Packages).filter(Packages.id > last_id).\
                    filter(Packages.updated > args.since). \
                    filter(Packages.existing).\
                    order_by(Packages.id).limit(10).all()
            else:
                package_stream = session.query(Packages).filter(Packages.id > last_id). \
                    filter(Packages.updated > args.since). \
                    filter(not Packages.existing).\
                    order_by(Packages.id).limit(10).all()
        else:
            if args.new_only:
                package_stream = session.query(Packages).filter(Packages.id > last_id). \
                    filter(not Packages.existing).\
                    order_by(Packages.id).limit(10).all()
            elif args.update_only:
                package_stream = session.query(Packages).filter(Packages.id > last_id). \
                    filter(Packages.existing).\
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

dumpfile = args.dumpfile
if dumpfile == '':
    dumpfile = 'geodump_{0}.jsonl'.format(datetime.now().strftime('%Y-%m-%d-%H%M%S'))
if args.new_only and args.update_only:
    print >> stderr, 'Cannot use --new-only and --update-only option at the same time'
main(since=args.since, dumpfile=dumpfile)

