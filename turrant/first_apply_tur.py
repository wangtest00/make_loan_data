from turrant.daihou_tur import *
from turrant.daiqian_tur import *
from database.dataBase_tur import *
from turrant.mgt_tur import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def first_apply():
    update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    token=login_code(registNo)
    insert_white_list(registNo)   #插入白名单数据。目前非黑非白，进件代码会拒件
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
    accType='12010001'  #类型选择绑银行卡，申请提现类型为银行卡
    if accType=='12010001':
        bank_no=bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(inter_db).call_many_proc()
        DataBase(inter_db).call_many_proc()
        approve(loanNo)
        sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
        DataBase(inter_db).executeUpdateSql(sql5)
        DataBase(inter_db).call_many_proc()
        #withdraw(custNo,loanNo,headt,headw,accType)
    else:
        bank_no = bank_auth_paytm(custNo, headt)
        update_appr_user_stat()
        DataBase(inter_db).call_many_proc()
        DataBase(inter_db).call_many_proc()
        approve(loanNo)
        sql5 = "update lo_loan_cust_rel set risk_level='AA',risk_score='" + prodNo + "' where LOAN_NO='" + loanNo + "';"
        DataBase(inter_db).executeUpdateSql(sql5)
        DataBase(inter_db).call_many_proc()
        withdraw(custNo, loanNo, headt, headw, '12010002')  #申请类型paytm
    # paytm_payout_webhook(loanNo)
    # time.sleep(3)
    # chaXun_Stat(loanNo)




if __name__ == '__main__':
    for i in range(10):
        first_apply()
