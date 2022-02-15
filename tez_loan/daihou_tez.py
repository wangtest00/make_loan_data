import json
import requests
from make_loan_data.database.dataBase_tez import *
from make_loan_data.data.var_tez_loan import *
from make_loan_data.public.check_api import *


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


#还款申请,还款金额只能等于应收表，待收金额！,金额不一致会报错{'errorCode': 30001, 'message': '参数为空'}
def re_payment_apply(loanNo):
    sql1="select RECEIVE_AMT from fin_ad_dtl where LOAN_NO='"+loanNo+"';"
    amt=DataBase(tez_db).get_one(sql1)
    transAmt=amt[0]
    if transAmt is None:
        print("应收表待收金额为空，不去还款申请，回调")
    else:
        sql="select CUST_NO,REPAY_DATE from lo_loan_dtl where LOAN_NO='"+loanNo+"';"
        custNox=DataBase(tez_db).get_one(sql)
        custNo=custNox[0]
        Repay_Date=custNox[1]
        data={"appNo": "301",
              "loanNo": loanNo,
              "custNo": custNo,
              "instNum": 1,
              "repayDate": Repay_Date,
              "transAmt": float(transAmt),
              "custName": "wangshang",
              "advance": "10000000",
              "isDefer": "10000000"}
        r=requests.post(host_pay+"/api/fin/re_payment/apply",data=json.dumps(data),headers=head_pay,verify=False)
        t=r.json()
        print(t)
        m=[]
        m.append(t['tranFlowNo'])
        m.append(t['globpayRepayment']['payOrderId'])
        m.append(t['globpayRepayment']['orderAmount'])
        print(m)
        return m
#还款模拟回调
def glopay_webhook_repay(mchOrderNo,payOrderId,orderAmount):
    paySuccessTime=str(time.time())
    paySuccessTime=paySuccessTime[:10]+paySuccessTime[11:14]
    data={
        "code": '1',
        "mchId": '1143',
        "mchOrderNo": mchOrderNo,
        "productId": '21',
        "orderAmount": int(float(orderAmount)*100),
        "payOrderId": payOrderId,
        "paySuccessTime": paySuccessTime,
        "message": '模拟回调放款成功',
        "extra": '',
        "sign": '111'
}
    #print(data)
    r=requests.post(host_pay+"/api/trade/globpay/webhook/repay",data=data,headers=head_pay_f,verify=False)
    print(r.content)
#申请还款，还款回调，结清
def glopay_apply_repay(loanNo):
    data=re_payment_apply(loanNo)
    glopay_webhook_repay(data[0],data[1],data[2])

if __name__ == '__main__':
    globpay_webhook_payout('L3012202158181813395073957888')
    #glopay_apply_repay('L3012202158181802724273848320')