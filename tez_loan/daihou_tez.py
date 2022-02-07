import requests,json,datetime
from make_loan_data.public.check_api import *
from make_loan_data.public.dataBase_tez import *
from make_loan_data.data.var_tez_loan import *

#放款-模拟回调
def globpay_webhook_payout(loan_no):
    sql="select TRAN_FLOW_NO,TRAN_ORDER_NO,SHD_TRAN_AMT from pay_tran_dtl where LOAN_NO='"+loan_no+"';"
    result=DataBase(tez_db).get_one(sql)
    print(result)
    amt=float('{0:f}'.format(result[2]))
    paySuccessTime=str(time.time())
    paySuccessTime=paySuccessTime[:10]+paySuccessTime[11:14]
    #放款模拟回调
    data={
    "code": '1',
    "mchId": '1143',
    "mchOrderNo": result[0],
    "productId": '16',
    "orderAmount": str(amt*100),
    "payOrderId": result[1],
    "paySuccessTime": paySuccessTime,
    "message": '模拟回调放款成功',
    "extra": '123456',
    "sign": '123'
}
    print(data)
    r=requests.post(host_pay+"/api/trade/globpay/webhook/payout",data,headers=head_pay_f,verify=False)
    print("调提现mock接口,响应=",r.content)
    if r.content==b'success':
        print("模拟回调,执行成功")
    else:
        print("模拟回调，执行失败")

def payout_apply(loanNo,custNo):
    data={
    "loanNo": loanNo,
    "custNo": custNo,
    "appNo": appNo
}
    r=requests.post(host_pay+"/api/fin/payout/apply",data=json.dumps(data),headers=head_pay,verify=False)
    print("调申请提现接口，请求Globpay",r.json())
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

@hulue_error()
def payout_mock_apply(loanNo,custNo):
    data={
    "loanNo": loanNo,
    "custNo": custNo,
    "appNo": "301"
}
    r=requests.post(host_pay+"/api/fin/payout/mock/apply",data=json.dumps(data),headers=head_pay,verify=False)
    print("调提现mock接口，暂时忽略报错",r.json())
if __name__ == '__main__':
    globpay_webhook_payout('L3012202078178927426834432000')
    #bank_open_annon_event('363636300062850013','10')