import io
import sys
from cashTm.daiqian_cashTm import *
from cashTm.daihou_cashTm import *
from cashTm.mgt_cashTm import *

#改编码方便jenkins运行
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
from requests.packages.urllib3.exceptions import InsecureRequestWarning

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
    sql2="update manage_need_loan.cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(inter_db).executeUpdateSql(sql2)
    sql3="update manage_need_loan.lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql3)
    sql4="update manage_need_loan.lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql4)
    time.sleep(5)
    token=login_code(registNo)
    headt=head_token(token)
    headw=head_token_w(token)
    auth(registNo,custNo,headt)
    loanNo=loan(registNo,custNo,headt)
    bank_no=bank_auth(custNo,headt)
    update_appr_user_stat()
    DataBase(inter_db).call_4_proc(inter_db)
    approve(loanNo)
    sql5="update manage_need_loan.lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql5)
    DataBase(inter_db).call_many_proc()
    withdraw_mock(custNo,loanNo,headt,headw)
    chaXun_Stat(loanNo)


if __name__ == '__main__':
    for i in range(1):
        first_apply()
