# -*- coding: UTF-8 -*-
# maintence robin <robin.chen@b-uxin.com>

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index,Numeric,DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import *
import os


Base = declarative_base()#SQLalchemy basic class

class models:

    def get_databse_connecton(self):
        # Open database config file
        fdc = open('db_config.ini', 'r')
        lines = fdc.readlines()
        db_list = {"mysql": "mysql+pymysql"}
        db_ini = {}
        for line in lines:
            index, value = line.split('=')
            db_ini[index] = value.strip()
        fdc.close()

        #add os environ setup for database connection
        if 'DB_HOST' in os.environ:
            db_ini['host'] = os.environ['DB_HOST']
        if 'DB_USER' in os.environ:
            db_ini['user'] = os.environ['DB_USER']
        if 'DB_PASSWD' in os.environ:
            db_ini['passwd'] = os.environ['DB_PASSWD']
        if 'DB_NAME' in os.environ:
            db_ini['db'] = os.environ['DB_NAME']
        if 'DB_PORT' in os.environ:
            db_ini['port'] = os.environ['DB_PORT']

        db_connect_string = "%s://%s:%s@%s:%s/%s?charset=%s" % (
        db_list['mysql'], db_ini['user'], db_ini['passwd'], db_ini['host'], db_ini['port'], db_ini['db'], db_ini['charset'])
        print(db_connect_string)

        return db_connect_string

    def get_engine(self):
        Engine = create_engine(self.get_databse_connecton(), echo=True)
        return Engine

    def get_session(self):
        Session = sessionmaker(bind=self.get_engine(), autocommit=False, autoflush=True)
        mysession = Session()
        return  mysession

    def init_db(self):
        Base.metadata.create_all(self.get_engine())

    def drop_table(self,table_name):
        pass


class Stocklist(Base):
    __tablename__ = 'stock_list'

    code = Column(String(6), primary_key=True, index=True)
    name = Column(String(16), index=True)

class Stockday_data(Base):
    __tablename__ = 'stock_data_day'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    code = Column(String(6), index=True)
    date = Column(DateTime, index=True)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    vol = Column(Numeric(10, 2))
    amount = Column(Numeric(10, 2))


"""
if __name__ == '__main__':

    orm = sqlorm()
    orm.create_tables()
    orm.Engine.execute("INSERT INTO stock_list (code,name) VALUES ('000737','中兴通讯')")
"""