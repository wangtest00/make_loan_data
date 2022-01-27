import json,random,requests,string
from make_loan_data.data.var_tez_loan import *
from make_loan_data.public.check_api import *
from make_loan_data.public.dataBase_tez import *
from make_loan_data.tez_loan.mgt_tez import *
from make_loan_data.tez_loan.daihou_tez import *
from make_loan_data.tez_loan.daiqian_tez import *

def first_apply():
    update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    token=login_code(registNo)
    headt=head_token(token)
    custNo=cert_auth(registNo,headt)
    auth(registNo,custNo,headt)
    update_kyc_auth(registNo,custNo)
    loanNo=loan(registNo,custNo,headt)
    lunXunDaiQian(loanNo)
    DataBase(tez_db).call_many_proc()
    time.sleep(3)
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(tez_db).executeUpdateSql(sql2)
    sql3="update lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';" #更新为撤销状态
    DataBase(tez_db).executeUpdateSql(sql3)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(tez_db).executeUpdateSql(sql4)
    time.sleep(5)
    token=login_code(registNo)
    headt=head_token(token)
    headw=head_token_w(token)
    auth(registNo,custNo,headt)
    loanNo=loan(registNo,custNo,headt)
    bank_auth(custNo,headt)
    update_appr_user_stat()
    DataBase(tez_db).call_many_proc()
    DataBase(tez_db).call_many_proc()
    approve(loanNo)
    sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(tez_db).executeUpdateSql(sql5)
    DataBase(tez_db).call_many_proc()
    status=withdraw(registNo,custNo,loanNo,headt,headw)  #该接口会调起支付payout_apply接口
    if status==1:
        time.sleep(3)
        globpay_webhook_payout(loanNo)
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


if __name__ == '__main__':
    for i in range(10):
        first_apply()
