from data.var_mex import *

from lanaPlus_duoqi.gaishu import *
from lanaPlus_duoqi.heads import *
from lanaPlus_duoqi.mex_mgt_lp import *


#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

#注册,认证，提交多种信息申请贷款
def first_login_apply(registNo):
    update_pwd(registNo)
    token=login_pwd(registNo)
    coupon_event_dispatch()
    headt=head_token(token)
    custNo=auth_cert(registNo,headt)
    coupon_event_dispatch()
    auth_work(custNo,headt)
    coupon_event_dispatch()
    auth_review_contact(custNo,headt)
    coupon_event_dispatch()
    auth_app_grab_data(registNo,custNo,headt)
    auth_contact(custNo,headt)
    coupon_event_dispatch()
    update_kyc_auth(registNo,custNo)
    #coupon_event_dispatch()
    update_batch_log()
    loan_no=apply_loan(custNo,headt)
    coupon_event_dispatch()
    if loan_no is None:
        DataBase(which_db).closeDB()
    else:
        bank_auth(custNo,headt)
        update_appr_user_stat()
        DataBase(which_db).call_4_proc()
        approve(loan_no)  #分配审批人员并审批通过
        coupon_event_dispatch()
        insert_risk(loan_no)
        w=withdraw(registNo,custNo,loan_no,headt)
        coupon_event_dispatch()
        if w==1:
            gaishu(loan_no)
            coupon_event_dispatch()
        else:
            pass
        DataBase(which_db).closeDB()
def auto_test():
    registNo=str(random.randint(8000000000,9999999999)) #10位随机数作为手机号
    first_login_apply(registNo)

#mex-扫描是否达到发放优惠券节点
def coupon_event_dispatch():
    print("开始等待63秒，满足条件：当前状态停留触发时间/分钟=1")
    time.sleep(63)
    r=requests.post('https://test-api.quantx.mx/api/cust/coupon/event/dispatch')
    print('扫描结果：',r.json())
    time.sleep(3)

if __name__ == '__main__':
    auto_test()
    #coupon_event_dispatch()