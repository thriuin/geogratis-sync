__author__ = 'Statistics Canada'
__copyright__ = 'Crown Copyright'
__license__ = 'MIT'

import requests
import simplejson as json
from db_schema import connect_to_database, GeogratisRecord, add_geogratis_record, find_geogratis_record
from time import sleep

def get_geogratis_rec(id, lang='en', data_format='json'):
    geog_url = 'http://geogratis.gc.ca/api/{0}/nrcan-rncan/ess-sst/{1}.{2}'.format(
        lang, id, data_format)
    r = requests.get(geog_url)
    if r.status_code == 200 and data_format == 'json':
        geo_result = r.json()
    else:
        print r.status_code
        geo_result = None
    sleep(1)
    return geo_result

def read_geogratis(since=''):
    geog_url = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst?alt=json'
    if since != '':
        geog_url = 'http://geogratis.gc.ca/api/en/nrcan-rncan/ess-sst?edited-min=%s&alt=json'.format(since)
    r = requests.get(geog_url)
    session = None
    try:
        session = connect_to_database()
        next_link = ''
        # Get the first page of the feed
        if r.status_code == 200:
            feed_page = r.json()
            for link in feed_page['links']:
                if link['rel'] == 'next':
                    next_link = link['href']
                    print next_link
                    break
            for product in feed_page['products']:
                save_geogratis_record(session, product['id'])
        # Keep polling until exhausted
        while next_link != '':
            geog_url = next_link
            r = requests.get(geog_url)
            feed_page = r.json()
            next_link = ''
            for link in feed_page['links']:
                if link['rel'] == 'next':
                    next_link = link['href']
                    print next_link
                    break
            for product in feed_page['products']:
                save_geogratis_record(session, product['id'])
    except Exception, e:
        print e
    finally:
        if not session is None:
            session.close_all()


def save_geogratis_record(session, uuid):
    print 'Retrieving data set {0}\n'.format(uuid)
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
        new_rec = find_geogratis_record(session, geo_rec_en['id'])

        if new_rec is None:
            new_rec = GeogratisRecord(uuid=geo_rec_en['id'],
                                      title_en=geo_rec_en['title'],
                                      title_fr=title_fr,
                                      json_record_en=json.dumps(geo_rec_en),
                                      json_record_fr=json.dumps(geo_rec_fr),
                                      created=geo_rec_en['createdDate'],
                                      updated=geo_rec_en['updatedDate'],
                                      edited=geo_rec_en['editedDate'],
                                      state=state)
        else:
            new_rec.title_en = geo_rec_en['title']
            new_rec.title_fr = title_fr
            new_rec.json_record_en = json.dumps(geo_rec_en)
            new_rec.json_record_fr = json.dumps(geo_rec_fr),
            new_rec.created = geo_rec_en['createdDate'],
            new_rec.updated = geo_rec_en['updatedDate'],
            new_rec.edited = geo_rec_en['editedDate'],
            new_rec.state = state

        add_geogratis_record(session, new_rec)


#print get_geogratis_rec('de667706-f3be-5fa8-b805-4c0908d7ca3f')
read_geogratis()



