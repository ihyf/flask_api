# coding:utf-8
from sqlalchemy import Column
from sqlalchemy import Integer, String, Text, JSON
from util.dbmanager import db_manager
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    # __bind_key__ = 'users_write'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Apps(Base):
    __tablename__ = 'apps'
    id = Column(Integer, autoincrement=True, primary_key=True)
    app_name = Column(String(200), primary_key=True)
    app_desc = Column(String(200))
    app_ip = Column(JSON)
    app_ns = Column(JSON)
    app_publickey = Column(Text)
    app_privateKey = Column(Text)
    app_function = Column(JSON)
    app_status = Column(Integer)


class Apps2(Base):
    __tablename__ = 'apps2'
    id = Column(Integer, autoincrement=True, primary_key=True)
    app_name = Column(String(200), primary_key=True)
    app_desc = Column(String(200))
    app_ip = Column(JSON)
    app_ns = Column(JSON)
    app_publickey = Column(Text)
    app_privateKey = Column(Text)
    app_function = Column(JSON)
    app_status = Column(Integer)
    app_request_times = Column(Integer)


def create_tables():
    engine = db_manager.get_engine_master()
    Base.metadata.create_all(engine)


