# -*- coding: UTF-8 -*-
# maintence rob

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import *
import os

class sqlorm:
    def __init__(self):
        # Open database config file
        fdc = open('db_config.ini', 'r')
        lines = fdc.readlines()
        db_list = {"mysql": "mysql+pymysql"}
        db_ini = {}
        for line in lines:
            index, value = line.split('=')
            db_ini[index] = value.strip()
        fdc.close()


        if 'DB_HOST' in os.environ:
            db_ini['host'] = os.environ['DB_HOST']
        if 'DB_USER' in os.environ:
            db_ini['user'] = os.environp['DB_USER']
        if 'DB_PASSWD' in os.environ:
            db_ini['passwd'] = os.environ['DB_PASSWD']
        if 'DB_NAME' in os.environ:
            db_ini['db'] = os.environ['DB_NAME']
        if 'PORT' in os.environ:
            db_ini['db'] = os.environ['PORT']

        db_connect_string = "%s://%s:%s@%s:%s/%s?charset=%s" % (db_list['mysql'], db_ini['user'], db_ini['passwd'], db_ini['host'], db_ini['port'], db_ini['db'],db_ini['charset'])
        print(db_connect_string)

        #create database
        #createdb = 'create DATABASE if not EXISTS %s' % db_ini['db']


        self.Engine = create_engine(db_connect_string, echo=True)
        self.Base = declarative_base()

        class stock_list(self.Base):
            __tablename__ = 'stock_list_test'
            code = Column(String(6),primary_key=True)
            name = Column(String(16))

    def create_tables(self):
        self.Base.metadata.create_all(self.Engine)

"""
if __name__ == '__main__':

    orm = sqlorm()
    orm.create_tables()
    orm.Engine.execute("INSERT INTO stock_list (code,name) VALUES ('000737','中兴通讯')")
"""