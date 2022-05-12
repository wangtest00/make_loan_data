import io
import sys
from turrant.daihou_tur import *
from turrant.daiqian_tur import *
from database.dataBase_tur import *
from turrant.mgt_tur import *
from data.var_tur import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from risk.risk import *

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#改编码方便jenkins运行
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

def first_apply_bank():
    sql = "UPDATE sys_app_info set PAY_CHAN_SERVICE='TurrantRazorpayTest' where app_no='"+appNo+"';"
    DataBase(inter_db).executeUpdateSql(sql)
    update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    token=login_code(registNo)
    insert_white_list(registNo)   #插入白名单数据。目前只有白名单用户才能进入风控走人审，其余一律拒绝
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
    sql5="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
    DataBase(inter_db).executeUpdateSql(sql5)
    india_thirdservice()     #调风控定时任务
    time.sleep(30)
    DataBase(inter_db).call_4_proc()  #分单去审批
    pl_shenpi()
    DataBase(inter_db).call_many_proc()  # 产品匹配
    withdraw(custNo,loanNo,headt,headw,'12010001')#类型选择绑银行卡，申请提现类型为银行卡
    pay_chan_service=cx_pay_chan_service()
    if pay_chan_service=='TurrantRazorpayTest':
        razorpayx_annon_event_callback(loanNo)
    else:
        print("当前产品的支付渠道=",pay_chan_service,"暂不模拟回调")
    time.sleep(3)
    chaXun_Stat(loanNo)


def first_apply_paytm():
    sql="UPDATE sys_app_info set PAY_CHAN_SERVICE='TurrantPaytmTest' where app_no='"+appNo+"';"
    DataBase(inter_db).executeUpdateSql(sql)
    update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    #registNo='9999189008'
    token=login_code(registNo)
    insert_white_list(registNo)   #插入白名单数据。目前只有白名单用户才能进入风控走人审，其余一律拒绝
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
    bank_no = bank_auth_paytm(custNo, headt)
    sql5 = "update lo_loan_cust_rel set risk_level='AA',risk_score='" + prodNo + "' where LOAN_NO='" + loanNo + "';"
    DataBase(inter_db).executeUpdateSql(sql5)
    india_thirdservice()    #调风控定时任务
    time.sleep(30)
    DataBase(inter_db).call_4_proc()   #分单
    pl_shenpi()
    DataBase(inter_db).call_many_proc() #产品匹配
    withdraw(custNo, loanNo, headt, headw, '12010002')  #申请类型paytm
    paytm_payout_webhook(loanNo,'SUCCESS')  #模拟提现成功，SUCCESS或失败，FAILURE
    time.sleep(3)
    chaXun_Stat(loanNo)

if __name__ == '__main__':
    for i in range(1):
        first_apply_bank()
        first_apply_paytm()
