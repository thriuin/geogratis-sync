__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import ckanapi
import logging
import simplejson as json

from ConfigParser import ConfigParser
from db_schema import connect_to_database, find_geogratis_record
from metadata_model import MetadataDatasetModel, MetadataResourcesModel


def create_model_geogratis(uuid):
    session = connect_to_database()
    geogratis_rec = find_geogratis_record(session, uuid)
    geo_rec_en = json.loads(geogratis_rec.json_record_en)
    geo_rec_fr = json.loads(geogratis_rec.json_record_fr)

    # Even if the French or English record is missing, create an object with
    return convert_geogratis_json(geo_rec_en, geo_rec_fr)


def create_model_ckan(uuid):
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_url = ini_config.get('ckan', 'ckan.remote_portal')

    ckansite = ckanapi.RemoteCKAN(remote_url)
    package = None
    try:
        package = ckansite.action.package_show(id=uuid)
    except Exception, e:
        logging.error(e)
    return convert_ckan_json(package)


def convert_geogratis_json(geo_obj_en, geo_obj_fr):

    ds = MetadataDatasetModel()

    # @TODO - Add the code that parses the Geogratis records and converts them a model object
    return ds


def convert_ckan_json(ckan_obj):

    ds = MetadataDatasetModel()

    # @TODO - Add the code that parses the CKAN records and converts them a model object

    return ds

