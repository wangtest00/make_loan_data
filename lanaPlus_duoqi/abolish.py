from database.dataBase_mex import *
from data.var_mex_lp_duoqi import *
from public.writeExcel import *
'''
将mex_pdl_loan库中注销用户相关表数据迁移至mex_pdl_abloish库中
'''

def get_TableName(column,database):
    sql="SELECT TABLE_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '"+database['database']+"' and COLUMN_NAME='"+column+"';"
    data=DataBase(database).get_all(sql)
    tableName=[]
    for data in data:
        tableName.append(data[0])
    print(tableName)
    return tableName

def get_forRegistNo(registNo,database):
    tableName=['cu_cust_contact_dtl', 'cu_cust_fee_rel', 'cu_cust_file_dtl', 'cu_cust_login_dtl','cu_cust_prod_rel', 'cu_cust_pwd_dtl', 'cu_cust_reg_dtl', 'lo_loan_cust_rel']
    sum=[]
    for tableName in tableName:
        sql="select * from "+database['database']+'.'+tableName+"  where regist_no='"+registNo+"';"
        sum.append(sql)
        res=DataBase(database).get_all(sql)
        if len(res)==0:
            sum.append('None')
        else:
            sum.append(str(res))
    n = 2  # 每2个一组等分 ,将一维列表转为二维列表
    sum = [sum[i:i + n] for i in range(0, len(sum), n)]
   # print(sum)
    return sum

def get_201(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if '201' in data[i][j]:
                print(data[i][j])
            else:
                pass
#全迁移存储过程
def quanQianYi(registNo):
    DataBase(configs).call_proc_args('201',registNo,procName='proc_pdl_table_backup_list')#调注销全迁移数据存储过程
#2个库包含表，筛选差异
def get_all():
    sql1="show tables;"
    data1=DataBase(mex_pdl_abolish).get_all(sql1)  #迁移库
    list1=[]
    for data1 in data1:
        list1.append(data1[0])
    print(list1)
    data2 = DataBase(configs).get_all(sql1)        #原库
    list2=[]
    for data2 in data2:
        list2.append(data2[0])
    print(list2)
    for list2 in list2:
        if list2 not in list1:#寻找差异，检查原库中的表哪些不在迁移库中
            print(list2)
        else:
            pass

def cx_Table(tableName,columnName,data,database):
    sum=[]
    for i in range(len(tableName)):
        sql="select * from "+tableName[i]+" where "+columnName+"='"+data+"';"
        sum.append(sql)
        res=DataBase(database).get_all(sql)
        if len(res)==0:
            sum.append('None')
        else:
            sum.append(str(res))
    n = 2  # 每2个一组等分 ,将一维列表转为二维列表
    sum = [sum[i:i + n] for i in range(0, len(sum), n)]
    return sum

def benfen_compare(registNo):
    path1 = os.path.join(os.getcwd(), '迁移前备份数据.xls')
    path2 = os.path.join(os.getcwd(), '迁移后查询结果.xls')
    sql="select CUST_NO from cu_cust_reg_dtl where REGIST_NO='"+registNo+"' and APP_NO='201';"
    custNo=DataBase(configs).get_one(sql)
    custNo=custNo[0]
    loanNo='L2012206208227407261048438784'
    sql2="INSERT INTO `mex_pdl_loan`.`cu_account_cancellation_record`(`ID`, `APP_NO`, `PHONE_NO`, `REASON`, `CUST_NO`, `CUST_NAME`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+registNo+'asdf'+registNo+"', '201', '"+registNo+"', 'wangtest', '"+custNo+"', 'AUTO SHUANG TEST', '2022-06-15 22:19:48', '"+custNo+"', NULL, NULL);"
    DataBase(configs).executeUpdateSql(sql2) #插入注销记录表数据
    tableName = get_TableName('CUST_NO', mex_pdl_abolish)
    value1 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, value1)
    # value2=get_forRegistNo(registNo, mex_pdl_loan)
    # WriteExcel().write_Xls_Append(path1, value2)
    # tableName3 = get_TableName('loan_no', mex_pdl_abolish)
    # value3 = cx_Table(tableName3, 'loan_no', loanNo, mex_pdl_loan)
    # WriteExcel().write_Xls_Append(path1, value3)
    quanQianYi(registNo)#调全迁移存储过程
    time.sleep(5)
    value4 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, value4)
    # value5 = get_forRegistNo(registNo, mex_pdl_abolish)
    # WriteExcel().write_Xls_Append(path2, value5)
    # value6 = cx_Table(tableName3,'loan_no', loanNo, mex_pdl_abolish)
    # WriteExcel().write_Xls_Append(path2, value6)
    if value1!=value4:
        print("CUST_NO相关表数据迁移不等")
    else:
        print("CUST_NO相关表数据迁移相等")
    # if value2!=value5:
    #     print("registNo相关表数据迁移不等")
    # else:
    #     print("registNo相关表数据迁移相等")
    # if value3!=value6:
    #     print("loan_no相关表数据迁移不等")
    # else:
    #     print("loan_no相关表数据迁移相等")

if __name__ == '__main__':
    benfen_compare('8218744452')