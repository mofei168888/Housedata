# -*- coding: UTF-8 -*-
# maintence robin <robin.chen@b-uxin.com>

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String, Date,ForeignKey, UniqueConstraint, Index,Numeric,DateTime
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
                            db_list['mysql'],
                            db_ini['user'],
                            db_ini['passwd'],
                            db_ini['host'],
                            db_ini['port'],
                            db_ini['db'],
                            db_ini['charset'])
        #print(db_connect_string)
        return db_connect_string

    def init_db(self):
        Base.metadata.create_all(self.get_engine())

    def get_engine(self):
        Engine = create_engine(self.get_databse_connecton(), echo=True)
        return Engine

    def get_session(self):
        Session = sessionmaker(bind=self.get_engine(), autocommit=False, autoflush=True)
        mysession = Session()
        return  mysession

    def get_connection(self):
        return self.get_session().connection()

    def drop_table(self,table_name):
        pass


class Stocklist(Base):
    __tablename__ = 'stock_list'

    code = Column(String(6), primary_key=True, index=True)
    name = Column(String(16), index=True)
    industry = Column(String(20))
    area = Column(String(10))
    pe = Column(Numeric(10, 2))
    outstanding = Column(Numeric(20, 2))
    totals = Column(Numeric(20, 2))
    totalAssets = Column(Numeric(20, 2))
    liquidAssets = Column(Numeric(20, 2))
    fixedAssets = Column(Numeric(20, 2))
    reserved = Column(Numeric(20, 2))
    reservedPerShare = Column(Numeric(20, 2))
    esp = Column(Numeric(20, 4))
    bvps = Column(Numeric(20, 2))
    pb = Column(Numeric(20, 2))
    timeToMarket = Column(String(10))
    undp = Column(Numeric(20, 2))
    perundp = Column(Numeric(20, 2))
    rev = Column(Numeric(20, 2))
    profit = Column(Numeric(20, 2))
    gpr = Column(Numeric(20, 2))
    npr = Column(Numeric(20, 2))
    holders = Column(Numeric(20,0))


class Stockday_data(Base):
    __tablename__ = 'ux_stock_data_day'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    code = Column(String(6), index=True)
    datetime = Column(DateTime, index=True)
    open = Column(Numeric(10, 2))
    high = Column(Numeric(10, 2))
    low = Column(Numeric(10, 2))
    close = Column(Numeric(10, 2))
    vol = Column(Numeric(20, 2))
    amount = Column(Numeric(20, 2))


"""
if __name__ == '__main__':

    
"""