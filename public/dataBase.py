# coding:utf-8
'''
Created on 2018-11-26
@author: 王爽
'''
import time
import pymysql
from data.var_mex import *


class DataBase():
    def __init__(self,witchdb):
        self.connectDB(witchdb)
    def connectDB(self,witchdb):
        try:
            self.connect=pymysql.connect(user=CONFIGS[witchdb]['user'],password=CONFIGS[witchdb]['password'],host=CONFIGS[witchdb]['host'],
                                         database=CONFIGS[witchdb]['database'],port=CONFIGS[witchdb]['port'], charset="utf8")
            self.cur=self.connect.cursor()
        except pymysql.Error as e:
            print(e)
    def get_all(self, sql):
        try:
            self.cur.execute(sql)
            value = self.cur.fetchall()
            return value
        except Exception as e:
            print("查询全部结果异常：",e)
            return 0
    def get_one(self,sql):
        try:
            self.cur.execute(sql)
            value = self.cur.fetchone()
            return value
        except Exception as e:
            print("查询单个结果异常：",e)
            return 0
    def closeDB(self):
        self.cur.close()
        self.connect.close()
    def executeUpdateSql(self,sql):
        try:
            self.cur.execute(sql)
            self.connect.commit()
            print ("更新表字段成功",sql)
            #self.closeDB()
        except Exception as e:
            print("更新异常：",e)
            return 0
    #调用mysql存储过程
    def call_proc(self,procName):
        try:
            self.cur.callproc(procName,args=("@o_stat",))
            self.connect.commit()
            print ("调用存储过程成功:",procName)
            #self.closeDB()
        except Exception as e:
            print("调用存储过程异常：",e)
            return 0
    def call_many_proc(self):
        proc=['proc_apr_loan_prod_sel','proc_apr_appr_all_user','proc_apr_appr_allocation','proc_apr_appr_allo_user_deal']
        for proc in proc:
            self.call_proc(proc)
        self.closeDB()
    def call_4_proc(self):
        for i in range(2):
            DataBase('mex_pdl_loan').call_many_proc()
            time.sleep(1)
#loanAmt='{0:f}'.format(t[0])#decimal转字符串

if __name__ == '__main__':
    DataBase('manage_need_loan').call_many_proc()
