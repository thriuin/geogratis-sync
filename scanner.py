__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import argparse
import logging
import requests
import simplejson as json
from datetime import datetime
from db_schema import connect_to_database, GeogratisRecord, add_record, find_record_by_uuid, Settings
from time import sleep

def _get_link(geo_page, link_rel='next'):
    next_link = ''
    for link in geo_page['links']:
        if link['rel'] == link_rel:
            next_link = link['href']
            logging.warn(next_link)
            break
    print 'Next link: {0}'.format(next_link)
    return next_link


def _get_setting(key_name):
    session = None
    setting_value = None
    try:
        session = connect_to_database()
        rec =session.query(Settings).filter(Settings.setting_name == key_name).one()
        setting_value = rec.setting_value
    except Exception, e:
        logging.error(e)
    finally:
        if not session is None:
            session.close_all()
    return setting_value


def _save_setting(key_name, key_value):
    setting = Settings()
    setting.setting_name = key_name
    setting.setting_value = key_value
    session = None
    try:
        session = connect_to_database()
        add_record(session, setting)
    except Exception, e:
        logging.error(e)
    finally:
        if not session is None:
            session.close_all()


def get_geogratis_rec(uuid, lang='en', data_format='json'):
    geog_url = 'http://geogratis.gc.ca/api/{0}/nrcan-rncan/ess-sst/{1}.{2}'.format(
        lang, uuid, data_format)
    r = requests.get(geog_url)
    if r.status_code == 200 and data_format == 'json':
        geo_result = r.json()
    else:
        logging.error('HTTP Error: {0}'.format(r.status_code))
        geo_result = None
    sleep(0.5)
    return geo_result


def read_geogratis(since='', start_index='', monitor=False):
    geog_url = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst?alt=json'
    if monitor:
        monitor_link = _get_setting('monitor_link')
        if not monitor_link:
            monitor_link = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst?edited-min=2015-01-01&alt=json'
        geog_url = monitor_link
    elif since != '':
        geog_url = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst?edited-min={0}&alt=json'.format(since)
    elif start_index != '':
        geog_url = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst/?start-index={0}&alt=json'.format(start_index)
    r = requests.get(geog_url)
    session = None
    try:
        session = connect_to_database()
        # Get the first page of the feed
        if r.status_code == 200:
            feed_page = r.json()

            # Save the monitor link for future use
            monitor_link = _get_link(feed_page, 'monitor')
            if monitor_link != '':
                _save_setting('monitor_link', monitor_link)

            next_link = _get_link(feed_page)

            print '{0} Records Found'.format(feed_page['count'])

            if 'products' in feed_page:
                for product in feed_page['products']:
                    try:
                        save_geogratis_record(session, product['id'])
                    except Exception, e:
                        logging.error('{0} failed to load'.format(product['id']))
                        logging.error(e)

            # Keep polling until exhausted
            while next_link != '':
                geog_url = next_link
                r = requests.get(geog_url)
                feed_page = r.json()            # Save the monitor link for future use
                monitor_link = _get_link(feed_page, 'monitor')
                if monitor_link != '':
                    _save_setting('monitor_link', monitor_link)
                next_link = _get_link(feed_page)
                if 'products' in feed_page:
                    for product in feed_page['products']:

                        # Don't crash on every call - log the error and continue
                        try:
                            save_geogratis_record(session, product['id'])
                        except Exception, e:
                            logging.error('{0} failed to load'.format(product['id']))
                            logging.error(e)

    except Exception, e:
        logging.error(e)
    finally:
        if not session is None:
            session.close_all()


def save_geogratis_record(session, uuid):
    msg = 'Retrieving data set {0}'.format(uuid)
    logging.info(msg)
    print(msg)
    geo_rec_en = get_geogratis_rec(uuid)
    geo_rec_fr = get_geogratis_rec(uuid, 'fr')
    if not geo_rec_en is None:
        state = 'deleted'
        title_fr = ''
        if geo_rec_en['deleted'] == 'false':
            state = 'active'
        if geo_rec_fr is None:
            state = 'missing french'
        else:
            title_fr = geo_rec_fr['title']
        new_rec = find_record_by_uuid(session, geo_rec_en['id'])

        created_date = '2000-01-01'
        updated_date = '2000-01-01'
        edited_date = '2000-01-01'
        geogratis_scanned = datetime.now().isoformat()
        if state != 'deleted':
            created_date = geo_rec_en['publishedDate']
            updated_date = geo_rec_en['updatedDate']
            edited_date = geo_rec_en['editedDate']

        if new_rec is None:
            new_rec = GeogratisRecord(uuid=geo_rec_en['id'],
                                      title_en=geo_rec_en['title'],
                                      title_fr=title_fr,
                                      json_record_en=json.dumps(geo_rec_en),
                                      json_record_fr=json.dumps(geo_rec_fr),
                                      created=created_date,
                                      updated=updated_date,
                                      edited=edited_date,
                                      state=state,
                                      geogratis_scanned=geogratis_scanned)
        else:
            new_rec.title_en = geo_rec_en['title']
            new_rec.title_fr = title_fr
            new_rec.json_record_en = json.dumps(geo_rec_en)
            new_rec.json_record_fr = json.dumps(geo_rec_fr),
            new_rec.created = created_date,
            new_rec.updated = updated_date,
            new_rec.edited = edited_date,
            new_rec.state = state
            new_rec.geogratis_scanned = geogratis_scanned

        add_record(session, new_rec)

argparser = argparse.ArgumentParser(
    description='Scan Geogratis and save record to a database'
)
argparser.add_argument('-d', '--since', action='store', default='', dest='since',
                       help='Scan since date (e.g. 2014-01-21)')
argparser.add_argument('-l', '--log', action='store', default='', dest='log_filename', help='Log to file')
argparser.add_argument('-s', '--start_index', action='store', default='', dest='start_index',
                       help='Start-index')
argparser.add_argument('-m', '--monitor', action='store_true', default=False, dest='monitor')

args = argparser.parse_args()

if args.log_filename != '':
    logging.basicConfig(filename=args.log_filename, level=logging.WARNING,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
print args.start_index
if args.monitor:
    read_geogratis('', '', True)
elif args.since != '':
    read_geogratis(since=args.since)
elif args.start_index != '':
    read_geogratis(start_index=args.start_index)
else:
    read_geogratis()
print 'Scan completed {0}'.format(datetime.now().isoformat())
