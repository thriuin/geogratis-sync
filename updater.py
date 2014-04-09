__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import ckanapi
from ConfigParser import ConfigParser
from datetime import datetime
from db_schema import connect_to_database, Packages, add_record
import json

def main():

    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_url = ini_config.get('ckan', 'ckan.remote_portal')
    api_key = ini_config.get('ckan', 'ckan.api_key')

    ckansite = ckanapi.RemoteCKAN(remote_url, apikey=api_key,
                                  user_agent='statcan_dataharvester/1.0 (+http://registry.data.gc.ca)')

    session = connect_to_database()
    last_id = 0
    while True:
        package_stream = session.query(Packages).filter(Packages.id > last_id)
        package_stream = package_stream.filter(Packages.status.in_(['new', 'update'])).\
                                               order_by(Packages.id).limit(10).all()

        if len(package_stream) == 0:
            break
        else:
            for r in package_stream:
                new_pkg_dict = json.loads(r.ckan_json.decode('utf-8'))
                try:
                    pkg_info = ckansite.action.package_show(id=r.uuid)
                    ckansite.call_action('package_update', new_pkg_dict)
                    r.status = 'posted'
                    r.latest_posted = datetime.now()
                    add_record(session, r)
                except ckanapi.NotFound:
                    ckansite.call_action('package_create', new_pkg_dict)
                    r.status = 'posted'
                    r.latest_posted = datetime.now()
                    add_record(session, r)
                    continue
                except ckanapi.NotAuthorized as e:
                    print u'Not Authorized {0}'.format(unicode(e))
                    continue
                except ckanapi.CKANAPIError as c:
                    print u'CKAN API error {0}'.format(unicode(c))
                    continue
                except ckanapi.ValidationError as v:
                    print u'Validation error {0}'.format(unicode(v.error_dict))
                    continue
            last_id = r.id
            break

main()