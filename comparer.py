__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

from ConfigParser import ConfigParser
import ckanapi
from datetime import datetime
from db_schema import connect_to_database, find_all_records, add_record, Packages, find_record_by_uuid
from geogratis_dataset_factory import MetadataDatasetModelGeogratisFactory
import json
import logging
from sys import stdout
import time

def get_od_package(uuid):
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_url = ini_config.get('ckan', 'ckan.remote_portal')

    ckansite = ckanapi.RemoteCKAN(remote_url)
    package = None
    try:
        package = ckansite.action.package_show(id=uuid)
    except Exception, e:
        logging.error(e.message)
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

    # Potentially doing a VERY large ORM query. If we don't limit the read, then SQLAlchemy will try to pull
    # everything into memory. Therefore the query must be paged. Paging requires keeping track of the sequential
    # record ID's

    session = connect_to_database()
    last_id = 0
    while True:
        known_records = find_all_records(session, query_limit=10, limit_id=last_id)

        if len(known_records) == 0:
            break
        else:
            for r in known_records:
                try:
                    # In order to avoid multiple updates, only allow for one instance of an update per uuid.
                    # Previous updates are overridden with the latest update
                    pkg_update = find_record_by_uuid(session, r.uuid, query_class=Packages)
                    if pkg_update is None:
                        pkg_update = Packages()
                    pkg_update.status = 'new'
                    if r.state == 'active':
                        ckan_record = factory.create_model_ckan(r.uuid)
                        geogratis_record = factory.create_model_geogratis(r.uuid)
                        pkg_update.uuid = r.uuid

                        # Set the dataset for immediate release on the Registry
                        geogratis_record.portal_release_date = time.strftime("%Y-%m-%d")
                        geogratis_record.ready_to_publish = True

                        if not ckan_record is None:

                            if not geogratis_record.equals(ckan_record):
                                diffs = geogratis_record.compare(ckan_record, self_label="Geogratis", other_label="CKAN")
                                r.differences = "\n".join(item for item in diffs)
                                pkg_update.od_status = 'Needs Update'
                                r.ckan_json = json.dumps(geogratis_record.as_dict())
                                pkg_update.status = 'update'
                            else:
                                pkg_update.od_status = 'Current'
                        else:
                            pkg_update.ckan_json = json.dumps(geogratis_record.as_dict())
                            pkg_update.od_status = 'New Record'
                    else:
                        pkg_update.od_status = 'Ineligible'
                    pkg_update.last_comparison = datetime.now()
                    add_record(session, r)
                    if pkg_update.od_status == 'New Record' or pkg_update.od_status == "Needs Update":
                        pkg_update.package = pkg_update.ckan_json
                        add_record(session, pkg_update)
                    last_id = r.id
                except Exception, e:
                    logging.error(e.message)
    session.close()


main()
