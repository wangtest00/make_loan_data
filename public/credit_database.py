# coding:utf-8
'''
Created on 2021-10-12
@author: 刘玲玲
'''
import time
import pymysql
from data.var_mex_credit import *
from make_loan_data.public.date_calculate import *

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
    def get_one(self,sql) -> object:
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
            self.closeDB()
        except Exception as e:
            print("更新异常：",e)
            return 0
    #调用mysql存储过程
    def call_proc(self,procName,date):
        try:
            self.cur.callproc(procName,args=(date,"@o_stat"))
            self.connect.commit()
            print ("调用存储过程成功:",procName,date)
            #self.closeDB()
        except Exception as e:
            print("调用存储过程异常：",e)
            return 0
    def call_batch_proc(self,date):
        proc=['proc_sys_batch_log_start','proc_fin_ad_record','proc_fin_ad_dtl','proc_sys_batch_log_end']
        for proc in proc:
            self.call_proc(proc,date)

#loanAmt='{0:f}'.format(t[0])#decimal转字符串
    def batch(self,date1,date2):
        sql="delete from sys_batch_log;"  #跑批前，先清空batch_log表跑批记录
        self.executeUpdateSql(sql)
        date_list=create_assist_date(date1,date2) #批量：从放款成功日期到账单日前一天
        for date_list in date_list:
            DataBase('mex_credit').call_batch_proc(date_list)
            time.sleep(3)
    def call_one_proc(self,procName):
        try:
            self.cur.callproc(procName,args=("@o_stat",))
            self.connect.commit()
            print ("调用存储过程成功:",procName)
            #self.closeDB()
        except Exception as e:
            print("调用存储过程异常：",e)
            return 0
    #分案存储过程
    def call_proc_apr_appr_allocation_control(self):
        for i in range(2):
            DataBase('mex_credit').call_one_proc('proc_apr_appr_allocation_control')
if __name__ == '__main__':
    #DataBase('mex_credit').batch('20211101','20211201')
    DataBase('mex_credit').batch('20211109','20211209')
   # DataBase('mex_credit').call_proc_apr_appr_allocation_control()


