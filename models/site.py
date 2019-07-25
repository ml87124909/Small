#coding: utf-8
from .model import  Base
from sqlalchemy import Column, Integer,Text


PREFIX = "site_"


class SiteMeta(Base):
    """ Site table """
    __tablename__ = PREFIX + "meta"

    id = Column(Integer, primary_key = True, nullable = False,autoincrement=True)
    name = Column(Text, nullable = True)
    value = Column(Text, nullable = True)




