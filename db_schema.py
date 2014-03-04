__author__ = 'thomros'

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

    def __repr__(self):
        return "<GeogratisRecord(id='%s'), title_en='%s', edited='%s'>" % (
            self.id, self.title_en, self.edited)


def connect_to_database():

    global Db_Session

    ini_config = ConfigParser()
    ini_config.read('geogratis.ini')
    db_url = ini_config.get('sqlalchemy', 'sqlalchemy.url')
    if Db_Session is None:
        engine = create_engine(db_url, echo=False)
        Db_Session = sessionmaker(bind=engine)
    return Db_Session()


def add_geogratis_record(session, geo_rec):

    session.add(geo_rec)
    session.commit()


def find_geogratis_record(session, uuid):

    rec = None
    try:
        rec = session.query(GeogratisRecord).filter(GeogratisRecord.uuid == uuid).one()
    except NoResultFound:
        # This is perfectly legit
        rec = None
    except MultipleResultsFound, e:
        print e
    return rec
