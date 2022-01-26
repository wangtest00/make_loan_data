import requests,json
from make_loan_data.public.check_api import *
from make_loan_data.public.dataBase_tez import *
from make_loan_data.data.var_tez_loan import *

@hulue_error()
def payout_mock_apply(loanNo,custNo):
    data={
    "loanNo": loanNo,
    "custNo": custNo,
    "appNo": appNo
}
    r=requests.post(host_pay+"/api/fin/payout/mock/apply",data=json.dumps(data),headers=head_pay,verify=False)
    print("调提现mock接口，暂时忽略报错",r.json())

def payout_apply(loanNo,custNo):
    data={
    "loanNo": loanNo,
    "custNo": custNo,
    "appNo": appNo
}
    r=requests.post(host_pay+"/api/fin/payout/apply",data=json.dumps(data),headers=head_pay,verify=False)
    print("调提现mock接口，暂时忽略报错",r.json())

def chaXun_Stat(loanNo):
    sql="select before_stat from lo_loan_dtl where loan_no='"+loanNo+"';"
    before_stat=DataBase(tez_db).get_one(sql)
    if before_stat[0]=='10260005':
        print("贷前状态已变更为:【已提现】",before_stat[0],loanNo)
    else:
        print("贷前状态未变更,查询到状态=",before_stat[0],loanNo)

def bank_open_annon_event(virtual_account_number,amount):
    '''bankopen-还款模拟回调'''
    data={"event_source":"virtual_account_payment",
   "event_types_id":4,
   "amount":amount,       #还款回调：目前只处理交易金额大于等于贷款金额的业务
   "bank_ref_id":"022216477238",
   "virtual_account_number":virtual_account_number,  #虚拟账户号
   "payment_date":"2020-08-09 16:37:58",
   "payment_mode":"UPI",
   "status":"success",
   "vpa":"open.3000002229@icici",
   "virtual_account_ifsc_code":"ICIC0000104",
   "name":"Faris Vendor 2",
   "primary_contact":"Faris2",
   "email_id":"johntest@gmail.com",
   "mobile_number":"1234567893",
   "hash":"c14b2100ee5bc68b54b468b99fd2208985aa27d138fbd523588644efba28d9a4"
}
    r=requests.post(host_pay+"/api/trade/bank_open/annon/event",data=json.dumps(data),headers=head_pay,verify=False)
    t=r.json()
    print(t)

if __name__ == '__main__':
    #payout_mock_apply('L1022108318120871775139594240','C1022108318120871626262773760')
    bank_open_annon_event('363636300062850013','10')