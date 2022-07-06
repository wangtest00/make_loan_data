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
    for data in data:   #排除无关表
        if data[0]=='fin_ad_detail_dtl_bk' or data[0]=='fin_ad_dtl_bk' or data[0]=='rpt_lo_repay_plan_dtl' or data[0]=='fin_ad_dtl' or data[0]=='fin_ad_detail_dtl':
            pass
        else:
            tableName.append(data[0])
    #print(tableName)
    return tableName


def get_forRegistNo(registNo,database):
    tableName=['cu_cust_contact_dtl', 'cu_cust_fee_rel', 'cu_cust_file_dtl', 'cu_cust_login_dtl','cu_cust_prod_rel', 'cu_cust_pwd_dtl', 'cu_cust_reg_dtl', 'lo_loan_cust_rel']
    sum=[]
    for tableName in tableName:
        sql="select * from "+tableName+"  where regist_no='"+registNo+"';"
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
    DataBase(mex_pdl_loan).call_proc_args('201',registNo,procName='proc_pdl_table_backup_list')#调注销全迁移数据存储过程
#2个库包含表，筛选差异
def get_all():
    sql1="show tables;"
    data1=DataBase(mex_pdl_abolish).get_all(sql1)  #迁移库
    list1=[]
    for data1 in data1:
        list1.append(data1[0])
    #print(list1)
    data2 = DataBase(mex_pdl_abolish_prod).get_all(sql1)        #生产库
    list2=[]
    for data2 in data2:
        list2.append(data2[0])
    #print(list2)
    for list1 in list1:
        if list1 not in list2:#检查迁移库中有无表不存在于生产库
            print(list1)
        else:
            pass
    return list1

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

def benfen_compare(registNo,loanNo):
    #应收，应收明细表不会迁移，因为注销客户，不会有应收
    path1 = os.path.join(os.getcwd(), '迁移前备份数据.xls')
    path2 = os.path.join(os.getcwd(), '迁移后查询结果.xls')
    sql="select CUST_NO from cu_cust_reg_dtl where REGIST_NO='"+registNo+"' and APP_NO='201';"
    custNo=DataBase(mex_pdl_loan).get_one(sql)
    custNo=custNo[0]
    if custNo is None:
        sql2 = "INSERT INTO `mex_pdl_loan`.`cu_account_cancellation_record`(`ID`, `APP_NO`, `PHONE_NO`, `REASON`, `CUST_NO`, `CUST_NAME`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + registNo + 'asdf' + registNo + "', '201', '" + registNo + "', 'wangtest', '', 'AUTO SHUANG TEST', '2022-06-15 22:19:48', '', NULL, NULL);"
        val1=''
        DataBase(mex_pdl_loan).executeUpdateSql(sql2)  # 插入注销记录表数据
    else:
        sql2 = "INSERT INTO `mex_pdl_loan`.`cu_account_cancellation_record`(`ID`, `APP_NO`, `PHONE_NO`, `REASON`, `CUST_NO`, `CUST_NAME`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + registNo + 'asdf' + registNo + "', '201', '" + registNo + "', 'wangtest', '" + custNo + "', 'AUTO SHUANG TEST', '2022-06-15 22:19:48', '" + custNo + "', NULL, NULL);"
        DataBase(mex_pdl_loan).executeUpdateSql(sql2)  # 插入注销记录表数据
        tableName = get_TableName('CUST_NO', mex_pdl_abolish)
        val1 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_loan)
        WriteExcel().write_Xls_Append(path1, val1)
    if loanNo=='':
        val3=''
    else:
        tableName3 = get_TableName('loan_no', mex_pdl_abolish)
        val3 = cx_Table(tableName3, 'loan_no', loanNo, mex_pdl_loan)
        WriteExcel().write_Xls_Append(path1, val3)
    val2=get_forRegistNo(registNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val2)
    tableName4=get_TableName('PHONE_NO', mex_pdl_abolish)
    val4=cx_Table(tableName4, 'PHONE_NO', registNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val4)
    val5=lingSan(registNo,loanNo,mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val5)
    quanQianYi(registNo)#调全迁移存储过程
    time.sleep(5)
    if custNo is None:
        val11=''
    else:
        tableName = get_TableName('CUST_NO', mex_pdl_abolish)
        val11 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_abolish)
        WriteExcel().write_Xls_Append(path2, val11)
    if loanNo == '':
        val33=''
    else:
        tableName3 = get_TableName('loan_no', mex_pdl_abolish)
        val33 = cx_Table(tableName3, 'loan_no', loanNo, mex_pdl_abolish)
        WriteExcel().write_Xls_Append(path2, val33)
    val22 = get_forRegistNo(registNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val22)
    tableName4 = get_TableName('PHONE_NO', mex_pdl_abolish)
    val44 = cx_Table(tableName4, 'PHONE_NO', registNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val44)
    val55 = lingSan(registNo, loanNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val55)
    if val1!=val11:
        print("CUST_NO相关表数据迁移不等")
    else:
        print("CUST_NO相关表数据迁移相等")
    if val2!=val22:
        print("registNo相关表数据迁移不等")
    else:
        print("registNo相关表数据迁移相等")
    if val3!=val33:
        print("loan_no相关表数据迁移不等")
    else:
        print("loan_no相关表数据迁移相等")
    if val4!=val44:
        print("PHONE_NO相关表数据迁移不等")
    else:
        print("PHONE_NO相关表数据迁移相等")
    if val5!=val55:
        print("lingsan相关表数据迁移不等")
    else:
        print("lingsan相关表数据迁移相等")

def benfen_compare_his(registNo,loanNo):
    # 应收，应收明细表不会迁移，因为注销客户，不会有应收
    path1 = os.path.join(os.getcwd(), '迁移前备份数据.xls')
    path2 = os.path.join(os.getcwd(), '迁移后查询结果.xls')
    sql = "select CUST_NO from cu_cust_reg_dtl where REGIST_NO='" + registNo + "' and APP_NO='201';"
    custNo = DataBase(mex_pdl_loan).get_one(sql)
    custNo = custNo[0]
    if custNo is None:
        sql2 = "INSERT INTO `mex_pdl_loan`.`cu_account_cancellation_record`(`ID`, `APP_NO`, `PHONE_NO`, `REASON`, `CUST_NO`, `CUST_NAME`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + registNo + 'asdf' + registNo + "', '201', '" + registNo + "', 'wangtest', '', 'AUTO SHUANG TEST', '2022-06-15 22:19:48', '', NULL, NULL);"
        val1 = ''
    else:
        sql2 = "INSERT INTO `mex_pdl_loan`.`cu_account_cancellation_record`(`ID`, `APP_NO`, `PHONE_NO`, `REASON`, `CUST_NO`, `CUST_NAME`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('" + registNo + 'asdf' + registNo + "', '201', '" + registNo + "', 'wangtest', '" + custNo + "', 'AUTO SHUANG TEST', '2022-06-15 22:19:48', '" + custNo + "', NULL, NULL);"
        tableName = get_TableName('CUST_NO', mex_pdl_abolish)
        val1 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_loan)
        WriteExcel().write_Xls_Append(path1, val1)
    DataBase(mex_pdl_loan).executeUpdateSql(sql2)  # 插入注销记录表数据
    if loanNo == '':
        val3 = ''
    else:
        tableName3 = get_TableName('loan_no', mex_pdl_abolish)
        val3 = cx_Table(tableName3, 'loan_no', loanNo, mex_pdl_loan)
        WriteExcel().write_Xls_Append(path1, val3)
    val2 = get_forRegistNo(registNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val2)
    tableName4 = get_TableName('PHONE_NO', mex_pdl_abolish)
    val4 = cx_Table(tableName4, 'PHONE_NO', registNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val4)
    val5 = lingSan(registNo, loanNo, mex_pdl_loan)
    WriteExcel().write_Xls_Append(path1, val5)
    DataBase(configs).call_proc_args('201', procName='proc_pdl_table_backup_list_his')  #处理历史注销表数据
    if custNo is None:
        val11=''
    else:
        tableName = get_TableName('CUST_NO', mex_pdl_abolish)
        val11 = cx_Table(tableName, 'CUST_NO', custNo, mex_pdl_abolish)
        WriteExcel().write_Xls_Append(path2, val11)
    if loanNo == '':
        val33=''
    else:
        tableName3 = get_TableName('loan_no', mex_pdl_abolish)
        val33 = cx_Table(tableName3, 'loan_no', loanNo, mex_pdl_abolish)
        WriteExcel().write_Xls_Append(path2, val33)
    val22 = get_forRegistNo(registNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val22)
    tableName4 = get_TableName('PHONE_NO', mex_pdl_abolish)
    val44 = cx_Table(tableName4, 'PHONE_NO', registNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val44)
    val55 = lingSan(registNo, loanNo, mex_pdl_abolish)
    WriteExcel().write_Xls_Append(path2, val55)
    DataBase(mex_pdl_loan).closeDB()
    DataBase(mex_pdl_abolish).closeDB()
    if val1!=val6:
        print("CUST_NO相关表数据迁移不等")
    else:
        print("CUST_NO相关表数据迁移相等")
    if val2!=val7:
        print("registNo相关表数据迁移不等")
    else:
        print("registNo相关表数据迁移相等")
    if val3!=val8:
        print("loan_no相关表数据迁移不等")
    else:
        print("loan_no相关表数据迁移相等")
    if val4!=val9:
        print("PHONE_NO相关表数据迁移不等")
    else:
        print("PHONE_NO相关表数据迁移相等")
    if val5!=val10:
        print("lingsan相关表数据迁移不等")
    else:
        print("lingsan相关表数据迁移相等")

def yichaTable(): #已做对比的3类表
    tableName = get_TableName('CUST_NO', mex_pdl_abolish)
    tableName3 = get_TableName('loan_no', mex_pdl_abolish)
    zuhedata = list(set(tableName +tableName3+ ['cu_cust_contact_dtl', 'cu_cust_fee_rel', 'cu_cust_file_dtl', 'cu_cust_login_dtl','cu_cust_prod_rel', 'cu_cust_pwd_dtl', 'cu_cust_reg_dtl', 'lo_loan_cust_rel']))
    print(zuhedata)
    return zuhedata

def xunzhao_Phone_No():
    data = yichaTable()
    table = get_TableName('PHONE_NO', mex_pdl_abolish)
    newdata = []
    for table in table:
        if table not in data:
            newdata.append(table)
        else:
            pass
    print(newdata)
    return newdata

def paiChufourData():
    data = yichaTable()
    newdata = xunzhao_Phone_No()
    y = list(set(data + newdata))
    alltable = get_all()
    fourdata = []
    for alltable in alltable:
        if alltable not in y:
            fourdata.append(alltable)
            #print(alltable)
        else:
            pass
    return fourdata

def lingSan(registNo,loanNo,database):
    sql1="select * from adjust_callback_data where match_id='"+registNo+"';"
    sql2="select * from cu_app_install_dtl where match_id='"+registNo+"';"
    sql3="select * from cu_coin_invite_dtl where INVITER='"+registNo+"';"
    sql4="select * from lo_auto_hand_record where busi_no='"+loanNo+"';"
    sql5="select * from lo_deci_decision_dtl where business_no='"+loanNo+"';"
    sql6="select * from lo_deci_order_dtl where business_no='"+loanNo+"';"
    sql7="select * from nxcdr_audio_file_deal_dtl where phone='"+registNo+"';"
    sql8="select * from nxcdr_callback_dtl where phone='"+registNo+"';"
    sql=[sql1,sql2,sql3,sql4,sql5,sql6,sql7,sql8]
    sum=[]
    for sql in sql:
        sum.append(sql)
        res = DataBase(database).get_all(sql)
        if len(res) == 0:
            sum.append('None')
        else:
            sum.append(str(res))
    n = 2  # 每2个一组等分 ,将一维列表转为二维列表
    sum = [sum[i:i + n] for i in range(0, len(sum), n)]
    return sum

def hebingtable(list1,list2,list3,list4):
    data=list(set(list1+list2+list3+list4))
    print(len(data))
    return data

def bidui_table(dbname):
    sql1='''SELECT
	TABLE_NAME,
	COLUMN_NAME
FROM
	information_schema.`COLUMNS` t
WHERE
	t.TABLE_SCHEMA = 'mex_pdl_loan'
and t.TABLE_NAME  in (
SELECT
	TABLE_NAME
FROM
	information_schema.`COLUMNS` t
WHERE
	t.TABLE_SCHEMA = 'mex_pdl_abolish'
GROUP BY
	TABLE_NAME

)
ORDER BY
	TABLE_NAME,
	COLUMN_NAME'''
    res=DataBase(dbname).get_all(sql1)
    print(res)
    return res

if __name__ == '__main__':
    #benfen_compare('8584830000','L2012206248228599068545449984')
    #benfen_compare('8888666666','')
    #benfen_compare_his('5412449999','')
    a=bidui_table(mex_pdl_loan)
    b=bidui_table(mex_pdl_loan_prod)
    if a==b:
        print("相同")