import sys,io
from turrant.daiHou import *
from turrant.daiQian import *
from database.dataBase_india import *
from turrant.mgt_Tur import *
from data.var_tur import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from risk.risk_for_india import *

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
'''
目前只有白名单和非黑非白用户才能进入风控走人审，其余一律拒绝
'''
def first_apply_bank():
    daiQian = DaiQian_Tur()
    sql = "UPDATE sys_app_info set PAY_CHAN_SERVICE='TurrantRazorpayTest' where app_no='"+appNo+"';"
    DataBase(configs).executeUpdateSql(sql)
    daiQian.update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    token=daiQian.login_code(registNo)
    daiQian.insert_white_list(registNo)   #插入白名单数据。
    headt=daiQian.head_token(token)
    custNo=daiQian.cert_auth(registNo,headt)
    daiQian.auth(registNo,custNo,headt)
    daiQian.update_kyc_auth(registNo,custNo)
    loanNo=daiQian.loan(registNo,custNo,headt)
    daiQian.lunXunDaiQian(loanNo)
    DataBase(configs).call_many_proc()
    time.sleep(3)
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(configs).executeUpdateSql(sql2)
    sql3="update lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';"
    DataBase(configs).executeUpdateSql(sql3)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(configs).executeUpdateSql(sql4)
    time.sleep(5)
    token=daiQian.login_code(registNo)
    headt=daiQian.head_token(token)
    headw=daiQian.head_token_w(token)
    daiQian.auth(registNo,custNo,headt)
    loanNo=daiQian.loan(registNo,custNo,headt)
    bank_no=daiQian.bank_auth(custNo,headt)
    sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(configs).executeUpdateSql(sql5)
    india_thirdservice()     #调风控定时任务
    time.sleep(5)
    update_appr_user_stat()           #更新审批人为上线状态
    DataBase(configs).call_4_proc()  #分单去审批
    DataBase(configs).call_4_proc()  # 分单去审批
    approve(loanNo)
    DataBase(configs).call_proc('proc_apr_loan_prod_sel')  # 产品匹配
    daiQian.withdraw(custNo,loanNo,headt,headw,'12010001')#类型选择绑银行卡，申请提现类型为银行卡
    pay_chan_service=daiQian.cx_pay_chan_service()
    if pay_chan_service=='TurrantRazorpayTest':
        daiQian.razorpayx_annon_event_callback(loanNo)
    else:
        print("当前产品的支付渠道=",pay_chan_service,"暂不模拟回调")
    time.sleep(3)
    DaiHou_tur().chaXun_Stat(loanNo)


def first_apply_paytm():
    daiQian = DaiQian_Tur()
    sql="UPDATE sys_app_info set PAY_CHAN_SERVICE='TurrantPaytmTest' where app_no='"+appNo+"';"
    DataBase(configs).executeUpdateSql(sql)
    daiQian.update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    #registNo='9999189008'
    token=daiQian.login_code(registNo)
    daiQian.insert_white_list(registNo)   #插入白名单数据。
    headt=daiQian.head_token(token)
    custNo=daiQian.cert_auth(registNo,headt)
    daiQian.auth(registNo,custNo,headt)
    daiQian.update_kyc_auth(registNo,custNo)
    loanNo=daiQian.loan(registNo,custNo,headt)
    daiQian.lunXunDaiQian(loanNo)
    DataBase(configs).call_many_proc()
    time.sleep(3)
    sql2="update cu_cust_dtl set RISK_LEVEL='AA',risk_score='"+prodNo+"' where cust_no='"+custNo+"';"
    DataBase(configs).executeUpdateSql(sql2)
    sql3="update lo_loan_dtl set BEFORE_STAT='10260007' where LOAN_NO='"+loanNo+"';"
    DataBase(configs).executeUpdateSql(sql3)
    sql4="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(configs).executeUpdateSql(sql4)
    time.sleep(5)
    token=daiQian.login_code(registNo)
    headt=daiQian.head_token(token)
    headw=daiQian.head_token_w(token)
    daiQian.auth(registNo,custNo,headt)
    loanNo=daiQian.loan(registNo,custNo,headt)
    bank_no = daiQian.bank_auth_paytm(custNo, headt)
    sql5 = "update lo_loan_cust_rel set risk_level='AA',risk_score='" + prodNo + "' where LOAN_NO='" + loanNo + "';"
    DataBase(configs).executeUpdateSql(sql5)
    india_thirdservice()    #调风控定时任务
    time.sleep(3)
    update_appr_user_stat()            #更新审批人为上线状态
    DataBase(configs).call_4_proc()   #分单
    DataBase(configs).call_4_proc()  # 分单去审批
    approve(loanNo)
    DataBase(configs).call_proc('proc_apr_loan_prod_sel')      #产品匹配
    daiQian.withdraw(custNo, loanNo, headt, headw, '12010002')  #申请类型paytm
    daiQian.paytm_payout_webhook(loanNo,'SUCCESS')  #模拟提现成功，SUCCESS或失败，FAILURE
    time.sleep(3)
    DaiHou_tur().chaXun_Stat(loanNo)

if __name__ == '__main__':
    for i in range(1):
        #first_apply_bank()
        first_apply_paytm()
