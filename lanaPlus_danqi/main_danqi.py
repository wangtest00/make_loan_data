import io
import sys
from lanaPlus_danqi.daihou_lp_danqi import *
from lanaPlus_danqi.gaishu_lp_danqi import *
from lanaPlus_danqi.daiqian_lp_danqi import *
from lanaPlus_danqi.mgt_lp_danqi import *
from data.var_mex_lp_danqi import *
#改编码方便jenkins运行
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#注册,认证，提交多种信息申请贷款到达待审批状态
def first_apply(registNo):
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    custNo=auth_cert(registNo,headt)
    auth_work(custNo,headt)
    auth_review_contact(custNo,headt)
    auth_app_grab_data(registNo,custNo,headt)
    auth_contact(custNo,headt)
    update_kyc_auth(registNo,custNo)
    update_batch_log()
    loan_no=apply_loan(custNo,headt)
    if loan_no is None:
        DataBase(which_db).closeDB()
    else:
        bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(which_db).call_4_proc()
        approve(loan_no)
        first_apply_sheipihou(loan_no,registNo,custNo,headt)

def first_apply_sheipihou(loan_no,registNo,custNo,headt):
    insert_risk(loan_no)#匹配产品
    #停在【通过】状态，用户待提现
    w=withdraw(registNo,custNo,loan_no,headt)  #app页面点击提现
    if w==1:
        gaishu(loan_no)
    else:
        pass
    DataBase(which_db).closeDB()
def auto_test():
    for i in range(2):
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        first_apply(registNo)
def make_tongguo():
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    custNo=auth_cert(registNo,headt)
    auth_work(custNo,headt)
    auth_review_contact(custNo,headt)
    auth_app_grab_data(registNo,custNo,headt)
    auth_contact(custNo,headt)
    update_kyc_auth(registNo,custNo)
    update_batch_log()
    loan_no=apply_loan(custNo,headt)
    if loan_no is None:
        DataBase(which_db).closeDB()
    else:
        bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(which_db).call_4_proc()
        approve(loan_no)  #分配审批人员并审批通过
        insert_risk(loan_no)
def apply_jieqing():
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    custNo=auth_cert(registNo,headt)
    auth_work(custNo,headt)
    auth_review_contact(custNo,headt)
    auth_app_grab_data(registNo,custNo,headt)
    auth_contact(custNo,headt)
    update_kyc_auth(registNo,custNo)
    update_batch_log()
    loan_no=apply_loan(custNo,headt)
    if loan_no is None:
        DataBase(which_db).closeDB()
    else:
        bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(which_db).call_4_proc()
        approve(loan_no)  #分配审批人员并审批通过
        first_apply_sheipihou(loan_no,registNo,custNo,headt)
        getRepayDateList_stp(registNo,loan_no,headt)

if __name__ == '__main__':
    auto_test()
    make_tongguo()
    apply_jieqing()