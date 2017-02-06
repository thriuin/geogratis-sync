import argparse
from ckanapi import RemoteCKAN, NotFound
from ConfigParser import ConfigParser


argparser = argparse.ArgumentParser(
    description='Purge the CKAN records based on a list of IDs in a file'
)
argparser.add_argument('-f', '--file', action='store', default='', dest='idfile',
                       help='File to read list of IDs from')
argparser.add_argument('-u', '--username', action='store', default='', dest='username',
                       help='CKAN username')
args = argparser.parse_args()


def main():
    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    remote_ckan_url = ini_config.get('ckan', 'ckan.url')
    remote_apikey = ini_config.get('ckan', 'ckan.sysadmin_apikey')
    # Create CKAN API connector to the portal
    ckan_portal = RemoteCKAN(remote_ckan_url, apikey=remote_apikey)

    f = open(args.idfile, 'r')
    for did in f:
        try:
            print did
            c = ckan_portal.action.package_show(id=did)
            print "Found {0}".format(did)
            continue
        except NotFound, n:
            pass
        ckan_portal.action.dataset_purge(id=did)

main()