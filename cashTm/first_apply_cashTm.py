from cashTm.daihou_cashTm import *
from cashTm.mgt_cashTm import *
from cashTm.daiqian_cashTm import *
from data.var_cashTm import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from risk.risk import *
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
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
    DataBase(inter_db).call_many_proc()
    time.sleep(3)
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(inter_db).executeUpdateSql(sql2)
    sql3="update lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql3)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql4)
    time.sleep(5)
    token=login_code(registNo)
    headt=head_token(token)
    headw=head_token_w(token)
    auth(registNo,custNo,headt)
    loanNo=loan(registNo,custNo,headt)
    bank_no=bank_auth(custNo,headt)
    DataBase(inter_db).call_4_proc(inter_db)
    time.sleep(10)
    approve(loanNo)
    #india_thirdservice()
    # time.sleep(30)
    sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql5)
    DataBase(inter_db).call_many_proc()
    withdraw_mock(custNo,loanNo,headt,headw)
    time.sleep(3)
    chaXun_Stat(loanNo)


if __name__ == '__main__':
    for i in range(1):
        first_apply()
