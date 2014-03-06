__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

from ConfigParser import ConfigParser
import simplejson as json
import ckanapi
from db_schema import connect_to_database, find_geogratis_record
import logging

def get_od_package(uuid):
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_url = ini_config.get('ckan', 'ckan.remote_portal')

    ckansite = ckanapi.RemoteCKAN(remote_url)
    package = None
    try:
        package = ckansite.action.package_show(id=uuid)
    except Exception, e:
        logging.error(e)
    return package


def compare_geo_ckan(geogratis_rec, ckan_rec):
    match = False
    print json.dumps(json.loads(geogratis_rec.json_record_en), indent=2 * ' ')
    print ckan_rec
    return match

# @TODO Given a list of UUID's, compare the scanned results from Geogratis with the record CKAN
#       Determine if the record has changed and really needs to be updated or not

session = connect_to_database()
geogratis_rec = find_geogratis_record(session, '2e17cbc0-2851-5947-896a-7429e7552bff')
ckan_rec = get_od_package('2e17cbc0-2851-5947-896a-7429e7552bff')

compare_geo_ckan(geogratis_rec, ckan_rec)
