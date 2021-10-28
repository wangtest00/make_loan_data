import string,requests,json,datetime,random
from make_loan_data.data.var_mex_credit import *
from make_loan_data.credit.heads import *
from make_loan_data.credit.daiqian import *
import io,sys
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

#注册,登录，提交多种信息，4项认证，待授信状态
def first_apply(registNo):
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    custNo=auth_cert(registNo,headt)
    update_kyc_auth(registNo,custNo)
    auth_work(custNo,headt)
    auth_app_grab_data(registNo,custNo,headt)
    auth_contact(custNo,headt)
    auth_review_contact(custNo,headt)
    auth_bank(custNo, headt)
    auth_review_bank(custNo,headt)
    risk_credit(headt)
    chaxun_risk_level(custNo)
    #time.sleep(3)
    #web_hook_payout_stp(custNo)   #模拟银行回调-放款

def auto_test():
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    first_apply(registNo)


if __name__ == '__main__':
    for i in range(1):
        auto_test()
