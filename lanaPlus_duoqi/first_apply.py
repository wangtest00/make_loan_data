import string,requests,json,datetime
from make_loan_data.public.dataBase import *
from make_loan_data.lanaPlus_duoqi.gaishu import *
from make_loan_data.lanaPlus_duoqi.mex_mgt_lp import *
from make_loan_data.lanaPlus_duoqi.heads import *
from make_loan_data.data.var_mex_lp import *
from make_loan_data.lanaPlus_duoqi.daihou import *
#import io,sys
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

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
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    first_apply(registNo)
#指定手机号，跑后续流程
def bu_ding(registNo):
    token=login_pwd(registNo)
    headt=head_token(token)
    sql="select CUST_NO from cu_cust_reg_dtl where REGIST_NO='"+registNo+"';"
    custNo=DataBase(which_db).get_one(sql)
    custNo=custNo[0]
    loan_no="L2012112068156388076948750336"
    if loan_no is None:
        DataBase(which_db).closeDB()
    else:
        bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(which_db).call_4_proc()
        approve(loan_no)  #分配审批人员并审批通过
        insert_risk(loan_no)
        w=withdraw(registNo,custNo,loan_no,headt)
        # if w==1:
        #     gaishu(loan_no)
        # else:
        #     pass
        # DataBase(which_db).closeDB()
def first_apply_curp(registNo):
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    custNo=auth_cert_curp(registNo,headt,"FYON990518MMFYONV8")
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

if __name__ == '__main__':
    for i in range(1):
        auto_test()
