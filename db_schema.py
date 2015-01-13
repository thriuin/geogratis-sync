__author__ = 'thomros'

import logging
from ConfigParser import ConfigParser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import UnicodeText, Date, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

# SQLalchemy MetaData object for the Geogratis tracking database.
Db_Session = None
g_base = declarative_base()

class GeogratisRecord(g_base):
    __tablename__ = 'geogratis_records'
    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UnicodeText)
    title_en = Column(UnicodeText)
    title_fr = Column(UnicodeText)
    created = Column(Date)
    updated = Column(Date)
    edited = Column(Date)
    state = Column(UnicodeText)
    json_record_en = Column(UnicodeText)
    json_record_fr = Column(UnicodeText)
    od_status = Column(UnicodeText)
    geogratis_scanned = Column(Date, nullable=True)


    def __repr__(self):
        return "<GeogratisRecord(id='%s'), title_en='%s', edited='%s'>" % (
            self.id, self.title_en, self.edited)

class Packages(g_base):
    __tablename__ = 'package_updates'
    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UnicodeText)
    created = Column(Date, nullable=True)
    updated = Column(Date, nullable=True)
    ckan_json = Column(UnicodeText, nullable=True)
    message = Column(UnicodeText, nullable=True)

def connect_to_database():

    global Db_Session

    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    db_url = ini_config.get('sqlalchemy', 'sqlalchemy.url')
    if Db_Session is None:
        engine = create_engine(db_url, echo=False)
        Db_Session = sessionmaker(bind=engine)
    return Db_Session()


def add_record(session, new_record):

    session.add(new_record)
    session.commit()


def find_record_by_uuid(session, uuid, query_class=GeogratisRecord):

    rec = None
    try:
        rec = session.query(query_class).filter(query_class.uuid == uuid).one()
    except NoResultFound:
        # This is perfectly legit
        rec = None
    except MultipleResultsFound, e:
        logging.error(e.message)
    except Exception, e:
        logging.error(e.message)
    return rec


def find_all_records(session, query_class=GeogratisRecord, query_limit=1000, limit_id=None):

    records = None
    try:
        if query_limit > 1000:
            query_limit = 1000
        if limit_id is None:
            limit_id = 0

        records = session.query(query_class).filter(query_class.id > limit_id).\
            order_by(query_class.id).limit(query_limit).all()
    except Exception, e:
        logging.error(e.message)
    return records