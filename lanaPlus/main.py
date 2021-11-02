import string,requests,json,datetime
from make_loan_data.public.dataBase import *
from make_loan_data.lanaPlus.gaishu import *
from make_loan_data.data.var_mex import *
from make_loan_data.lanaPlus.mex_mgt import *
from make_loan_data.lanaPlus.heads import *
import io,sys
#改编码方便jenkins运行
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

#注册,认证，提交多种信息申请贷款
def first_login_apply(registNo):
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
        w=withdraw(registNo,custNo,loan_no,headt)
        if w==1:
            gaishu(loan_no)
        else:
            pass
        DataBase(which_db).closeDB()
def auto_test():
    for i in range(1):
        registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
        first_login_apply(registNo)


if __name__ == '__main__':
    auto_test()
    #gaishu('L2012106088090503701168824320')