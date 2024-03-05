from typing import Any
import time

import scrapy
from sqlalchemy.orm import sessionmaker

from tutorial.spiders.flats import Base, Flat, Image

from tutorial.settings import DATABASE
import retrying
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


# Retry decorator to retry the database connection
@retrying.retry(
    stop_max_attempt_number=5,  # Maximum number of retry attempts
    wait_fixed=5000,            # Wait 2 seconds between each retry
    retry_on_exception=lambda x: isinstance(x, OperationalError)
)
def connect_to_database():
    # Attempt to create a database connection
    engine = create_engine(f"{DATABASE['drivername']}://{DATABASE['username']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}")
    try:
        connection = engine.connect()
        connection.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise
    return engine


class SrealitySpider(scrapy.Spider):
    name = 'sreality_spider'
    allowed_domains = ['www.sreality.cz']
    start_urls = [f'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&per_page=20&page={i}'
                  for i in range(1, 26)]

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.engine = connect_to_database()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def write_to_table(self, flat_name: str, image_url: str):
        with self.Session() as session:
            flat = session.query(Flat).filter(Flat.name == flat_name).first()
            if not flat:
                flat = Flat(name=flat_name)
                session.add(flat)
                session.flush()  # Flush to get flat.id
            session.expunge(flat)
            session.add(flat)
            image = Image(url=image_url, flat_id=flat.id)
            session.add(image)
            session.commit()

    def parse(self, response):
        json_response = response.json()
        estates = json_response['_embedded']['estates']
        time.sleep(2)
        for estate in estates:
            for image_url in estate['_links']['images']:
                self.write_to_table(flat_name=estate['name'], image_url=image_url['href'])

