from ckanapi import RemoteCKAN, NotFound
from ConfigParser import ConfigParser
from db_schema import connect_to_database, GeogratisRecord
from geogratis_dataset_factory import MetadataDatasetModelGeogratisFactory
from sys import stderr


def main():
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_ckan_url = ini_config.get('ckan', 'ckan.url')

    factory = MetadataDatasetModelGeogratisFactory()

    # Create CKAN API connector to the portal
    ckan_portal = RemoteCKAN(remote_ckan_url, user_agent='converter/1.0 http://open.canada.ca/data')

    # Page through the datasets on

    session = connect_to_database()
    last_id = 0

    try:
        while True:
            ckan_records = ckan_portal.action.package_search(
                q='extras_collection:geogratis AND extras_org_title_at_publication:"Natural Resources Canada"',
                rows=100,
                start=last_id)
            if not ckan_records:
                break
            else:
                for r in ckan_records['results']:
                    rp = session.query(GeogratisRecord).filter(GeogratisRecord.uuid == r['name']).all()
                    if not rp:
                        print r
            last_id += 100
    except Exception, e:
        print >> stderr, e.message
        pass
    session.close()


main()
