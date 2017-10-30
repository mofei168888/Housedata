# -*- coding: UTF-8 -*-

import pymysql

class mydb:

    def __init__(self):
        dbini = open('db_config.ini','r') #Open database config file
        mydbini = {'database': 'Mysql'}
        lines = dbini.readlines()
        for line in lines:
            index,value = line.split('=')
            mydbini[index]=value.strip()
        dbini.close()
        try:
           self.connect =  pymysql.Connect(host= mydbini['host'],
                                      port=int(mydbini['port']),
                                      user=mydbini['user'],
                                      passwd=mydbini['passwd'],
                                      db=mydbini['db'],
                                      charset=mydbini['charset'])
        except Exception as e:
            print("Open Database Error："+str(e))
        else:
            self.cur = self.connect.cursor()

    def select_records(self,column,table,condition):
        strsql = 'select '+column + ' from '+table+ ' where '+condition
        #print(strsql)
        try:
            self.recordcount = self.cur.execute(strsql)
            lines = self.cur.fetchall()
        except Exception as e:
            print('select sql error:'+str(e))
        return lines

    def select_allrecords(self, column, table):
        strsql = 'select ' + column + ' from ' + table
        try:
            self.recordcount = self.cur.execute(strsql)
            lines = self.cur.fetchall()
        except Exception as e:
            print('select sql error:' + str(e))
        return lines

    def update_record(self,table,colval,condition):
        strsql = 'update '+ table+' set '+colval +' where '+condition
        try:
            self.recordcount = self.cur.execute(strsql)
        except Exception as e:
            self.connect.rollback()
            print('update sql error:'+str(e))
            self.msg = "Update Failed"
        else:
            self.connect.commit()
            self.msg = "Update Success"

    def insert_record(self, table, value):
        strsql = 'insert into '+table +' values ('+value+ ')'
        try:
            self.recordcount = self.cur.execute(strsql)
        except Exception as e:
            self.connect.rollback()
            print('Insert sql error:' + str(e))
            self.msg = "Insert Failed"
            self.flag = 0
        else:
            self.connect.commit()
            self.msg = "Insert Success"
            self.flag = 1

    def delete_record(self,table,condition):
        strsql = 'delete from '+ table + ' where '+condition
        try:
            self.recordcount = self.cur.execute(strsql)
        except Exception as e:
            self.connect.rollback()
            print('delete sql error:' + str(e))
            self.msg = "delete sql error:"+str(e)
            self.flag = 0
        else:
            self.connect.commit()
            self.msg = "delete Success"
            self.flag = 1

    def getvalueformat(self,items):
        str = ''
        for i in items.values():
            str+="'"+i+"',"

        return str.strip(',')

    def getfieldformat(self, items):
        str = ''
        for i in items:
            str +=(i + ",")

        return str.strip(',')


    def close_db(self):
        self.cur.close()
        self.connect.close()
