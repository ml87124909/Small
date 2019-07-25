#coding: utf-8
from .model import Base
from sqlalchemy import Column, Integer,Text,DateTime

PREFIX = ""


class User(Base):
    """ user table """
    __tablename__ = PREFIX + "user"
    id = Column(Integer, primary_key = True, nullable=False,autoincrement=True)
    username = Column(Text,  nullable=True)
    nickname = Column(Text,  nullable=True)
    password =  Column(Text,  nullable=True)
    avatar = Column(Text,  nullable=True)
    updatetime = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, nullable=True)

    




