__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import ckanapi
from ConfigParser import ConfigParser
from datetime import datetime
from db_schema import connect_to_database, Packages, add_record
from time import sleep
import json

def main():

    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_url = ini_config.get('ckan', 'ckan.remote_portal')
    api_key = ini_config.get('ckan', 'ckan.api_key')
    user_agent = ini_config.get('ckan', 'ckan.user_agent')

    ckansite = ckanapi.RemoteCKAN(remote_url, apikey=api_key,
                                  user_agent=user_agent)

    session = connect_to_database()
    last_id = 0
    while True:
        package_stream = session.query(Packages).filter(Packages.id > last_id)
        package_stream = package_stream.filter(Packages.status.in_(["new", "update"])).\
                                               order_by(Packages.id).all()

        if len(package_stream) == 0:
            break
        else:
            for r in package_stream:
                sleep(60)
                print u'Processing dataset {0}'.format(r.id)
                try:
                    new_pkg_dict = json.loads(r.ckan_json.decode('utf-8'))
                except AttributeError as a:
                    print u'AttributeError {0}'.format(unicode(a))
                    continue
                is_new = False
                try:
                    pkg_info = ckansite.action.package_show(id=r.uuid)
                except ckanapi.NotFound:
                    is_new = True
                try:
                    if is_new:
                        ckansite.call_action('package_create', new_pkg_dict)
                    else:
                        ckansite.call_action('package_update', new_pkg_dict)
                    r.status = 'posted'
                    r.status_message = ''
                    r.latest_posted = datetime.now()
                    add_record(session, r)
                    continue
                except ckanapi.NotAuthorized as e:
                    print u'Not Authorized {0}'.format(unicode(e))
                    continue
                except ckanapi.CKANAPIError as c:
                    r.status = 'error'
                    r.status_message = u'CKAN API error {0}'.format(unicode(c))
                    add_record(session, r)
                    print r.status_message
                    continue
                except ckanapi.errors.ValidationError as v:
                    r.status = 'error'
                    r.status_message = u'Validation error {0}'.format(unicode(v.error_dict))
                    add_record(session, r)
                    print r.status_message
                    continue
            break

main()