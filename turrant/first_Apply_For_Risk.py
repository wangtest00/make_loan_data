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

def first_apply():
    daiQian = DaiQian_Tur()
    daiQian.update_Batch_Log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    #daiQian.insert_white_list(registNo)
    token=daiQian.login_code(registNo)
    headt=daiQian.head_token(token)
    custNo=daiQian.cert_auth(registNo,headt)
    daiQian.auth(registNo,custNo,headt)
    daiQian.update_kyc_auth(registNo,custNo)
    loanNo=daiQian.loan(registNo,custNo,headt)
    print(loanNo)
    india_thirdservice()     #调风控定时任务


if __name__ == '__main__':
    first_apply()
