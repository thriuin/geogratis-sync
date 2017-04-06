import argparse
from ckanapi import RemoteCKAN, NotFound
from ConfigParser import ConfigParser
import sys
from time import sleep

argparser = argparse.ArgumentParser(
    description='Read a list of Geogratis UUIDs from stdin and delete'
)
argparser.add_argument('-c', '--config', action='store', default='development.ini', dest='configfile',
                       help='Config file')
argparser.add_argument('-f', '--file', action='store', default='', dest='idfile',
                       help='File to read list of IDs from')
args = argparser.parse_args()


def main():

    ini_config = ConfigParser()
    ini_config.read(args.configfile)
    remote_ckan_url = ini_config.get('ckan', 'ckan.url')
    remote_apikey = ini_config.get('ckan', 'ckan.apikey')
    # Create CKAN API connector to the portal

    ckan_portal = RemoteCKAN(remote_ckan_url, apikey=remote_apikey)

    try:
        f = open(args.idfile, 'r')
        for line in f:
            try:
                # If the record does not exist, then a NotFound exception will be thrown
                pkg_id = str(line).strip()
                pkg = ckan_portal.action.package_show(id=pkg_id)
                # Only Geogratis records will be deleted
                if pkg['collection'] == 'geogratis':
                    ckan_portal.action.dataset_purge(id=pkg_id)
                    print >> sys.stdout, '{0} deleted'.format(pkg_id)
                else:
                    print >> sys.stderr, '{0} is not a GeoGratis dataset'.format(pkg_id)
                sleep(5)
            except NotFound, e:
                print >> sys.stderr, 'Unable to locate dataset {0}'.format(pkg_id)
                pass
    except IOError:
        print >> sys.stderr, 'Error while reading line.'

main()

