from database.dataBase_mex import *
#from public.writeExcel import *
from public.writeExcel2 import *
'''
#查询CUST_NO在哪些表中包含
select table_name from information_schema.tables where table_schema='mex_pdl_loan' and table_type='base table'
AND TABLE_NAME IN(
    SELECT DISTINCT TABLE_NAME  FROM information_schema.COLUMNS WHERE COLUMN_NAME = 'CUST_NO' AND TABLE_SCHEMA='mex_pdl_loan' AND TABLE_NAME NOT LIKE 'CUST_NO%'
)
;'''
def cx_db_write(tableName,custNo):
    sum_list=[]
    for tableName in tableName:
        sql1="select * from "+tableName+" where CUST_NO='"+custNo+"';"
        sql2="select COLUMN_NAME from information_schema.COLUMNS where table_name = '"+tableName+"' and table_schema = 'mex_pdl_loan';" #查询表中的所有字段名
        s1=DataBase('mex_pdl_loan').get_all(sql1)
        sum_res=[]
        for j in range(len(s1)):
            sum_res.append(list(s1[j]))#元组转列表
        for i in range(len(sum_res)):
            for k in range(len(sum_res[i])):
                sum_res[i][k]=str(sum_res[i][k])
        res2=DataBase('mex_pdl_loan').get_all(sql2)
        column_name=[]
        for res2 in res2:
            column_name.append(res2[0])
        #print(column_name)
        sql=[]
        sql.append(sql1)
        sum_res.insert(0,sql)         #插入sql语句
        sum_res.insert(1,column_name) #保存表中所有字段名
        sum_res.append(['占位'])
        # print(sum_res)
        sum_list=sum_list+sum_res   #二维列表合并在一起
    print(sum_list)
    WriteExcel().write_for_cx_db_write(sum_list)

if __name__ == '__main__':
    cx_db_write(["apr_appr_pool_dtl",'cu_cust_auth_dtl','cu_cust_cert_dtl'],'C2012102038045509285306597376')