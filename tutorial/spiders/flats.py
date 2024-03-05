from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Flat(Base):
    __tablename__ = 'flats'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    images = relationship("Image", back_populates="flat")


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    flat_id = Column(Integer, ForeignKey('flats.id'))
    flat = relationship("Flat", back_populates="images")

