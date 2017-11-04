# -*- coding: UTF-8 -*-
#MAINTAINER Robin<robin.chen@b-uxin.com>
#Version V.0001


from pytdx.hq import  TdxHq_API
from pytdx.params import TDXParams
import pandas as pd
import tushare as ts
import os
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


if __name__ == '__main__':

   #print("test")
   #get_history_data('000737',20171003)
   #data = ts.get_st_classified()
   #print(data)

   print("start insert into mysql database!")
   model = models()
   model.init_db()

   session = model.get_session()

   #每次执行时清空表
   session.query(Stocklist).delete()
   session.commit()

   counter = 0
   while 1:
      stock = Stocklist(code='%s'%counter, name='中兴通讯')
      session.add(stock)
      session.commit()
      counter +=1
