#coding:utf-8

from sqlalchemy import create_engine,Column, Integer,Text,DateTime,SMALLINT#, Table, Column, Integer, Text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
PREFIX="book_"
from dbconfig import tiger,scott,host,port,dbname
url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % (scott, tiger, host,port,dbname)
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)


class User(Base):
    """ user table """
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    username = Column(Text,  nullable=True)
    nickname = Column(Text,  nullable=True)
    password =  Column(Text,  nullable=True)
    avatar = Column(Text,  nullable=True)
    updatetime = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=True)

class SiteMeta(Base):
    """ Site table """
    __tablename__ =  "meta"

    id = Column(Integer, primary_key = True, nullable = False,autoincrement=True)
    name = Column(Text, nullable = True)
    value = Column(Text, nullable = True)


class Book(Base):

    __tablename__ =PREFIX + "book"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    name = Column(Text, nullable=True)
    access = Column(Integer,  nullable=True)
    status = Column(Integer,nullable=True)       # publish status
    select_catalog = Column(Integer,nullable=True)
    publish_timestamp = Column(DateTime,  nullable=True)
    updatetime = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=True)
    cover = Column(Text, nullable=True)


class BookCatalog(Base):

    __tablename__ = PREFIX+"catalog"

    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    title = Column(Text,  nullable=True)
    markdown =Column(Text,  nullable=True)
    html = Column(Text,  nullable=True)
    publish_markdown =Column(Text,  nullable=True)
    publish_html = Column(Text,  nullable=True)
    status = Column(Integer, nullable = True)
    abstract = Column(Text, nullable = True)
    publish_order = Column(Integer,  nullable=True)
    pos = Column(Integer,  nullable=True)
    parent_id = Column(Integer,nullable=True)
    is_dir = Column(SMALLINT, nullable=True)
    publish_timestamp = Column(DateTime, nullable=True)
    first_publish = Column(DateTime,  nullable=True)
    updatetime = Column(DateTime, nullable=True)
    timestamp = Column(DateTime,nullable=True)

    book_id = Column(Integer,nullable=True)


class BookImage(Base):

    __tablename__ =PREFIX + "image"
    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    name = Column(Text,  nullable=True)
    filename = Column(Text, nullable=True)
    book_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, nullable=True)

def createall(engine_):
    try:
        Base.metadata.drop_all(engine_)
    except:
        pass
    Base.metadata.create_all(engine_)