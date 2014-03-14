__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

from ConfigParser import ConfigParser
import simplejson as json
import ckanapi
from db_schema import connect_to_database, find_geogratis_record
from metadata_model_factory import MetadataDatasetModelGeogratisFactory
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

    match = geogratis_rec.equals(ckan_rec)
    if not match:
        diffs = geogratis_rec.compare(ckan_rec)
        for d in diffs:
            print d
    #print json.dumps(json.loads(geogratis_rec.json_record_en), indent=2 * ' ')
    #print json.dumps(ckan_rec, indent=2 * ' ')
    return match

# @TODO Given a list of UUID's, compare the scanned results from Geogratis with the record CKAN
#       Determine if the record has changed and really needs to be updated or not

factory = MetadataDatasetModelGeogratisFactory()

ckan_record = factory.create_model_ckan('2e17cbc0-2851-5947-896a-7429e7552bff')

geogratis_record = factory.create_model_geogratis('2e17cbc0-2851-5947-896a-7429e7552bff')

compare_geo_ckan(geogratis_record, ckan_record)
