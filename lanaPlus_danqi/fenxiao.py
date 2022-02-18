import requests,json
from make_loan_data.data.var_mex_lp_duoqi import *
from make_loan_data.lanaPlus_danqi.daiqian_lp_danqi import *

#三级分销-用户调提现接口
def withdraw(phoneNo,money,headt):
    data={"phoneNo":phoneNo,"smallestWithdrawAmt":"100","withdrawAmt":money}
    r=requests.post(host_api+'/api/cust/promote/withdraw',data=json.dumps(data),headers=headt)
    print(r.json())

if __name__ == '__main__':
    token=login_pwd('8667722222')
    headt=head_token(token)
    withdraw('8667722222','5000000',headt)#测试用很大的金额去提现