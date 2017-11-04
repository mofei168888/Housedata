# -*- coding: UTF-8 -*-
# maintence robin <robin.chen@b-uxin.com>



import pandas as pd
import tushare as ts

try:
    from app.models import *
except Exception as e:
    from models import *


def get_history_data(code, date):
    ST_TYPE = {'6': 1,  # 0 深圳，1 上海
               '3': 0,
               '0': 0}

    api = TdxHq_API()
    flag = 0
    try:
        api.connect()
    except Exception as e:
        print("connect Error:" + str(e))
    else:
        # print(ST_TYPE[code[0][0]])  # 获取股票代码的第一位，判断属于哪一个交易所
        # data = api.get_history_minute_time_data(ST_TYPE[code[0][0]], code, date)
        try:
            data = api.get_history_minute_time_data(ST_TYPE[code[0][0]], code, date)
            print("CODE:" + code + ",Date:" + str(date) + ",Type:" + str(ST_TYPE[code[0][0]]))
        except Exception as e:
            print("Error:" + str(e))
        else:
            frames = api.to_df(data)
            #df = pd.concat(frames, axis=1)
            print(frames)
            flag = 1
    return flag



class StockData:
    def __init__(self):
        self.model = models()
        self.model.drop_table()
        self.model.init_db()
        self.db_session = self.model.get_session()

    def insert_stocklist(self):

        # 每次执行时清空表
        self.db_session.query(Stocklist).delete()
        self.db_session.commit()

        # 插入股票列表数据
        df = ts.get_stock_basics().reset_index()
        df.to_sql(Stocklist.__tablename__, self.model.get_engine(), if_exists='append', index=False)

        #pdf = pd.read_sql_table('stock_list', self.model.get_connection())


    def get_stocklist(self):
        return self.db_session.query(Stocklist).order_by(Stocklist.code).all()

    def insert_stock_data(self):
        #清空数据表
        self.db_session.query(Stockday_data).delete()
        self.db_session.commit()

        #插入股票交易日数据

        PERIOD = ('D')
        stocklist = self.get_stocklist()
        for sl in stocklist:
            print("code:%s,name:%s" % (sl.code, sl.name))
            try:
                df = ts.bar(sl.code, ktype=PERIOD[0]).reset_index()
            except Exception as e:
                print("get stock:%s network error!"%sl.code)
            finally:
                df.to_sql(Stockday_data.__tablename__, self.model.get_engine(), if_exists='append', index=False)

