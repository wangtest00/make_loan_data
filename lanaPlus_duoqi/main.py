from lanaPlus_duoqi.daiHou import *
from lanaPlus_duoqi.gaiShu_mex import *
from lanaPlus_duoqi.daiQian import *
from lanaPlus_duoqi.mgt_Duoqi import *
from data.var_mex_lp_duoqi import *
from common.calculate import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from database.dataBase_mex import *
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
    if loan_no is None:
        DataBase(configs).closeDB()
    else:
        daiQian.bank_auth(custNo, headt)
        update_appr_user_stat()
        DataBase(configs).call_4_proc()
        approve(loan_no)
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
    for i in range(2):
        registNo = str(random.randint(8000000000, 9999999999))
        first_apply(registNo)

def make_tongguo():
    daiQian = DaiQian_Duoqi()
    daiQian.update_batch_log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    code=compute_code(registNo)
    token=daiQian.login_code(registNo,code)
    headt=head_token(token)
    custNo=daiQian.auth_cert(registNo,headt)
    daiQian.auth_work(custNo,headt)
    daiQian.auth_review_contact(custNo,headt)
    daiQian.auth_app_grab_data(registNo,custNo,headt)
    daiQian.auth_contact(custNo,headt)
    daiQian.update_kyc_auth(registNo,custNo)
    loanNo=daiQian.apply_loan(custNo,headt)
    if loanNo is None:
        DataBase(configs).closeDB()
    else:
        daiQian.bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(configs).call_4_proc()
        approve(loanNo)  #分配审批人员并审批通过
        MockData().insert_risk(loanNo)

def apply_jieqing():
    daiQian = DaiQian_Duoqi()
    daiHou=DaiHou()
    daiQian.update_batch_log()
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    code = compute_code(registNo)
    token = daiQian.login_code(registNo, code)
    headt = head_token(token)
    custNo=daiQian.auth_cert(registNo,headt)
    daiQian.auth_work(custNo,headt)
    daiQian.auth_review_contact(custNo,headt)
    daiQian.auth_app_grab_data(registNo,custNo,headt)
    daiQian.auth_contact(custNo,headt)
    daiQian.update_kyc_auth(registNo,custNo)
    loan_no=daiQian.apply_loan(custNo,headt)
    if loan_no is None:
        DataBase(configs).closeDB()
    else:
        daiQian.bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(configs).call_4_proc()
        approve(loan_no)  #分配审批人员并审批通过
        sheiPiHou(loan_no,registNo,custNo,headt)
        daiHou.getRepayDateList_stp(registNo,loan_no,headt)

if __name__ == '__main__':
    auto_test()
    make_tongguo()
    apply_jieqing()