from tez_loan.daiqian_tez import *
from tez_loan.mgt_tez import *
from tez_loan.daihou_tez import *
from tez_loan.heads_tez import *
from database.dataBase_tez import *
from data.var_tez_loan import *

#目前需求：非黑非白的客户进件直接拒绝，且不进审批池
def first_apply():
    update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    sql="INSERT INTO `cu_white_list_dtl`(`ID`, `WHITE_LIST_TYPE`, `WHITE_LIST_VALUE`, `APP_NO`, `RISK_SCORE`, `USEABLE`, `VALID_START_DATE`, `VALID_END_DATE`, `ORIGIN`, `DESCRIPTION`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+registNo+"', '10140001', '"+registNo+"', '301', '10003', '10000001', '20220208', '20220508', '"+registNo+"', NULL, NULL, '2022-02-08 11:13:25', 'wangs2@quantditech.com', '2022-02-15 16:01:30', 'wangs2@quantditech.com');"
    DataBase(tez_db).executeUpdateSql(sql)
    custNo=login_code(registNo)
    headt=head_token(custNo[0])
    custNo=custNo[1]
    custNo=cert_auth(registNo,custNo,headt)
    auth(registNo,custNo,headt)
    update_kyc_auth(registNo,custNo)
    loanNo=loan(registNo,custNo,headt)  #第一次申请后会被拒，因为无评级和评分
    lunXunDaiQian(loanNo)
    DataBase(tez_db).call_many_proc()
    time.sleep(3)
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(tez_db).executeUpdateSql(sql2)
    sql3="update lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';" #更新为撤销状态
    DataBase(tez_db).executeUpdateSql(sql3)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(tez_db).executeUpdateSql(sql4)
    time.sleep(5)#再次进件
    custNo2=login_code(registNo)
    headt=head_token(custNo2[0])
    headw=head_token_w(custNo2[0])
    custNo=cert_auth(registNo,custNo,headt)
    auth(registNo,custNo,headt)
    update_kyc_auth(registNo,custNo)
    loanNo=loan(registNo,custNo,headt)
    bank_auth(custNo,headt)
    update_appr_user_stat()
    DataBase(tez_db).call_many_proc()
    DataBase(tez_db).call_many_proc()
    approve(loanNo)
    sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(tez_db).executeUpdateSql(sql5)
    DataBase(tez_db).call_many_proc()
    status=withdraw(registNo,custNo,loanNo,headt,headw)#该接口会调起支付payout_apply接口
    if status==1:
        time.sleep(10)
        globpay_webhook_payout(loanNo)#模拟回调-放款成功    注意现在是模拟查询返成功，投产前需要改成查询三方放款订单状态
        time.sleep(3)
        chaXun_Stat(loanNo)
    else:
        print(status)

def chaXunDaiQian(loanNo):
    sql1="select BEFORE_STAT from lo_loan_dtl where LOAN_NO='"+loanNo+"';"
    before_stat=DataBase(tez_db).get_one(sql1)
    before_stat=before_stat[0]
    return before_stat
def lunXunDaiQian(loanNo):
    for t in range(1):
        before_stat=chaXunDaiQian(loanNo)
        if before_stat=='10260006':
            break
        else:
            time.sleep(3)
            print("贷前状态未变更为拒绝")
            continue

#重新进件待审批后，去更新评分并审批
def buding(custNo,loanNo):
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(tez_db).executeUpdateSql(sql2)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(tez_db).executeUpdateSql(sql4)
    DataBase(tez_db).call_many_proc()
    DataBase(tez_db).call_many_proc()
    approve(loanNo)
    DataBase(tez_db).call_many_proc()

if __name__ == '__main__':
    for i in range(1):
        first_apply()
    #buding('C3012202148181434714541686784','L3012202148181436195936305152')