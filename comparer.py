__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

from ConfigParser import ConfigParser
import ckanapi
from datetime import datetime
from db_schema import connect_to_database, find_all_geogratis_records, add_geogratis_record
from geogratis_dataset_factory import MetadataDatasetModelGeogratisFactory
import json
import logging
from sys import stdout

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
        print '{0} Does not match'.format(geogratis_rec.id)
        # diffs = geogratis_rec.compare(ckan_rec, self_label="Geogratis", other_label="CKAN")
        # for d in diffs:
        #     print d
    else:
        print '{0} Matches'.format(geogratis_rec.id)
        print json.dump(geogratis_rec.as_dict(), stdout, indent=2)
    #print json.dumps(ckan_rec, indent=2 * ' ')
    return match

# @TODO Given a list of UUID's, compare the scanned results from Geogratis with the record CKAN
#       Determine if the record has changed and really needs to be updated or not

def main():

    factory = MetadataDatasetModelGeogratisFactory()
    session = connect_to_database()
    known_records = find_all_geogratis_records(session)
    for r in known_records:
        try:
            if r.state == 'active':
                ckan_record = factory.create_model_ckan(r.uuid)
                geogratis_record = factory.create_model_geogratis(r.uuid)
                if not ckan_record is None:
                    if not geogratis_record.equals(ckan_record):
                        diffs = geogratis_record.compare(ckan_record, self_label="Geogratis", other_label="CKAN")
                        r.differences = "\n".join(item for item in diffs)
                        r.ckan_json = json.dumps(geogratis_record.as_dict())
                        r.od_status = 'Needs Update'
                    else:
                        r.od_status = 'Current'
                else:
                    r.ckan_json = json.dumps(geogratis_record.as_dict())
                    r.od_status = 'New Record'
            else:
                r.od_status = 'Ineligible'
            r.last_comparison = datetime.now()
            add_geogratis_record(session, r)
        except Exception, e:
            logging.error(e)
    session.commit()
    session.close()

main()
