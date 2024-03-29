from backUp.daiHou import *
from backUp.gaiShu_mex import *
from backUp.daiQian import *
from data.var_mex_backup import *
from common.calculate import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from database.dataBase_mex import *
from risk.risk_for_mex import *
from backUp.heads_mex import *
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import io,sys
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

# 注册,认证，提交多种信息申请贷款到达待审批状态
def first_apply(registNo):
    daiQian=DaiQian_Duoqi()
    daiQian.update_batch_log()
    code=compute_code(registNo)
    token=daiQian.login_code(registNo,code)
    headt = head_token(token)
    daiQian.update_pwd(registNo, headt)
    custNo = daiQian.auth_cert(registNo, headt)
    daiQian.auth_work(custNo, headt)
    daiQian.auth_review_contact(custNo, headt)
    daiQian.auth_app_grab_data(registNo, custNo, headt)
    daiQian.auth_contact(custNo, headt)
    daiQian.update_kyc_auth(registNo, custNo)
    loan_no = daiQian.apply_loan(custNo, headt)
    mex_thirdservice()
    if loan_no is None:
        DataBase(configs).closeDB()
    else:
        daiQian.bank_auth(custNo, headt)
        DataBase(configs).call_4_proc()
        sheiPiHou(loan_no, registNo, custNo, headt)

def sheiPiHou(loanNo, registNo, custNo, headt):
    daiQian = DaiQian_Duoqi()
    MockData().insert_risk(loanNo)  # 匹配产品
    #停在【通过】状态，用户待提现
    w = daiQian.withdraw(registNo, custNo, loanNo, headt)  # app页面点击提现
    if w == 1:
        MockData().gaishu(loanNo)
    else:
        pass
    DataBase(configs).closeDB()

def auto_test():
    for i in range(1):
        registNo = str(random.randint(8000000000, 9999999999))
        first_apply(registNo)



if __name__ == '__main__':
    auto_test()
