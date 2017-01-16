from db_schema import connect_to_database, GeogratisRecord, get_setting
import argparse
from ckanapi import RemoteCKAN, NotFound
from ConfigParser import ConfigParser

__author__ = 'Statistics Canada'

argparser = argparse.ArgumentParser(
    description='Print a list of Geogratis UUIDs whose state has been set to "deleted"'
)
argparser.add_argument('-f', '--file', action='store', default='', dest='dumpfile',
                       help='File to write UUIDs to')
argparser.add_argument('-m', '--monitor', action='store_true', default=False, dest='monitor')
args = argparser.parse_args()


def main():
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_ckan_url = ini_config.get('ckan', 'ckan.url')
    # Create CKAN API connector to the portal
    ckan_portal = RemoteCKAN(remote_ckan_url, user_agent='converter/1.0 http://open.canada.ca/data')

    last_id = 0
    last_run_setting = get_setting('last_conversion_run')
    session = connect_to_database()

    while True:
        if args.monitor:

            geogratis_stream = session.query(GeogratisRecord).filter(GeogratisRecord.id > last_id)\
                .filter(GeogratisRecord.state == 'deleted')\
                .filter(GeogratisRecord.updated > last_run_setting.setting_value)\
                .order_by(GeogratisRecord.id).limit(10).all()
        else:
            geogratis_stream = session.query(GeogratisRecord).filter(GeogratisRecord.id > last_id)\
                .filter(GeogratisRecord.state == 'deleted')\
                .order_by(GeogratisRecord.id).limit(10).all()

        if len(geogratis_stream) == 0:
            break
        else:
            for r in geogratis_stream:

                # Determine if the record is already on the OD portal
                try:
                    ckan_portal.action.package_show(id=r.uuid)
                    # If the record does not exist, then a NotFound exception will be thrown
                    print u'{0}'.format(r.uuid)
                except NotFound, e:
                    pass
                last_id = r.id

    session.close()

main()
