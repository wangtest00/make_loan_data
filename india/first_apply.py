import json,random,requests,string
from data.var_india import *
from public.check_api import *
from india.daiqian_cashTM import *
from public.dataBase import *

def first_apply():
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    token=login_code(registNo)
    headt=head_token(token)
    custNo=cert_auth(registNo,headt)
    auth(registNo,custNo,headt)
    loanNo=loan(registNo,custNo,headt)
    lunXunDaiQian(loanNo)
    DataBase(inter_db).call_many_proc()
    time.sleep(3)
    sql2="update manage_need_loan.cu_cust_dtl set RISK_LEVEL='AA',risk_score='1' where cust_no='"+custNo+"';"
    DataBase(inter_db).executeUpdateSql(sql2)
    sql3="update manage_need_loan.lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql3)
    # cert_auth(registNo,headt)
    # auth(registNo,custNo,headt)
    # loanNo=loan(registNo,custNo,headt)

def chaXunDaiQian(loanNo):
    sql1="select BEFORE_STAT from manage_need_loan.lo_loan_dtl where LOAN_NO='"+loanNo+"';"
    before_stat=DataBase(inter_db).get_one(sql1)
    before_stat=before_stat[0]
    return before_stat
def lunXunDaiQian(loanNo):
    for t in range(10):
        before_stat=chaXunDaiQian(loanNo)
        if before_stat=='10260006':
            break
        else:
            time.sleep(3)
            print("贷前状态未变更为拒绝")
            continue


if __name__ == '__main__':
    first_apply()
