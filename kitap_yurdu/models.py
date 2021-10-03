from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from scrapy.utils.project import get_project_settings


engine = create_engine('sqlite:///sales.db', echo = True)
Base = declarative_base()

Session = sessionmaker(bind = engine)
session = Session()

class Book_Library(Base):
    __tablename__ = 'library'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    writer = Column(String)
    publisher = Column(String)
    price = Column(String)
    publish_date = Column(String)
    page_number = Column(String)
    external_link = Column(String)
    rating_score = Column(String)
    review_counts = Column(String)
    description = Column(String)


def connect_db():
    return create_engine('sqlite:///books.db')


def create_table(engine):
    return Base.metadata.create_all(engine)