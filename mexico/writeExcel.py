# coding=UTF-8
'''
20190507
注意，文件在本地打开的时候不能删除
'''
import xlrd,datetime
import xlwt,os
from xlutils.copy import copy
from public.dataBase import *

class WriteExcel(object):
    def write_Excel_Xls(self):
        now = datetime.datetime.now()
        nowtime=str(now.strftime('%Y%m%d'))
        book_name_xls=os.path.join(os.getcwd(),'xls格式测试工作簿'+nowtime+'.xls')
        sheet_name_xls = 'xls格式测试sheet表单'
        value_title = [["接口URL", "请求方式", "请求参数", "测试结果","响应状态码", "响应数据"],]
        path=book_name_xls
        sheet_name=sheet_name_xls
        value=value_title
        index = len(value)  # 获取需要写入数据的行数
        workbook = xlwt.Workbook()  # 新建一个工作簿
        sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
        workbook.save(path)  # 保存工作簿
        print("xls格式表格写入数据成功！")
    def write_Excel_Xls_Append(self, value):
        now = datetime.datetime.now()
        nowtime=str(now.strftime('%Y%m%d'))
        book_name_xls=os.path.join(os.getcwd(),'xls格式测试工作簿'+nowtime+'.xls')
        path=book_name_xls
        index = len(value)  # 获取需要写入数据的行数
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
        for i in range(0, index):
            for j in range(0, len(value[i])):
                new_worksheet.write(i+rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(path)  # 保存工作簿
        print("xls格式表格【追加】写入数据成功！")
    def read_Excel_Xls(self):
        now = datetime.datetime.now()
        book_name_xls = 'C:\\Users\\wangshuang\\Desktop\\210603_Mex_风控模型压力测试同步测试环境数据500单_ws.xls'
        path=book_name_xls
        workbook = xlrd.open_workbook(path)  # 打开工作簿
        sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
        for i in range(0, worksheet.nrows):
            for j in range(0, worksheet.ncols):
                # 逐行逐列读取数据
                t=worksheet.cell_value(i,j)
                #print(t)
                # sql="UPDATE lo_deci_order_dtl set SERVICE_PROD_NO='WK122300_New_OwnRules',ORDER_NO=NULL,STATUS=NULL,START_TIME=NULL,inst_time=NULL,CALLBACK_TIME=null,CALLBACK_VALUE=NULL where BUSINESS_NO='"+t+"';"
                # DataBase(which_db).executeUpdateSql(sql)
                # sql2="DELETE from lo_deci_decision_dtl where BUSINESS_NO='"+t+"';"
                # DataBase(which_db).executeUpdateSql(sql2)
                sql3="select CALLBACK_VALUE from lo_deci_order_dtl where BUSINESS_NO='"+t+"';"
                s3=DataBase(which_db).get_one(sql3)
                print(s3[0])

if __name__ == '__main__':
    value1 = [["张三", "男", "19", "杭州", "研发工程师"],
              ["李四", "男", "22", "北京", "医生"],
              ["王五", "女", "33", "珠海", "出租车司机"],]
    value2 = [["Tom", "男", "21", "西安", "测试工程师","123","456","789",'000'],
              ["Jones", "女", "34", "上海", "产品经理"],
              ["Cat", "女", "56", "上海", "教师"],]
    #每次要创建一个新的xls文件，新的表单
    #WriteExcel().write_Excel_Xls()
    #WriteExcel().write_Excel_Xls_Append(value1)
    WriteExcel().read_Excel_Xls()