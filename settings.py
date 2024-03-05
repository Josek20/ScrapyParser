from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tutorial.settings import DATABASE
from tutorial.spiders.flats import Base

engine = create_engine(
    DATABASE['drivername'] + '://' + DATABASE['username'] + ':' + DATABASE['password'] + '@' + DATABASE[
        'host'] + ':' + DATABASE['port'] + '/' + DATABASE['database'])
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
FLATS_PER_PAGE = 20
