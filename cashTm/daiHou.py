import json,time
import requests
from database.dataBase_india import *
from public.check_api import *
from data.var_cashTm import *

t=str(time.time()*1000000)[:10]
head_pay_for_razorpay={"Host":"test-pay.quantstack.in","Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
    "User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br","X-Razorpay-Event-Id":"HDSG"+t,"X-Razorpay-Signature":"cashtm9527"}
class DaiHou_CashTm():
    @hulue_error()
    def payout_mock_apply(self,loanNo,custNo):
        data={
        "loanNo": loanNo,
        "custNo": custNo,
        "appNo": appNo,
        "accType": "12010001"   #12010001=银行卡，12010002=PayTm Wallet
    }
        print(data)
        r=requests.post(host_pay+"/api/fin/payout/mock/apply",data=json.dumps(data),headers=head_pay,verify=False)
        print("调提现mock接口，暂时忽略报错",r.json())

    def chaXun_Stat(self,loanNo):
        sql="select before_stat from lo_loan_dtl where loan_no='"+loanNo+"';"
        before_stat=DataBase(configs).get_one(sql)
        if before_stat[0]=='10260005':
            print("贷前状态已变更为:【已提现】",before_stat[0],loanNo)
        else:
            print("贷前状态未变更,查询到状态=",before_stat[0],loanNo)
    #bankopen-还款模拟回调，注意：记得先要申请还款,创建bankopen账户,调api,trade_fin_repay函数
    def bank_open_annon_event(self,virtual_account_number,amount):
        '''bankopen-还款模拟回调'''
        data={"event_source":"virtual_account_payment",
       "event_types_id":6,    #非4，则支付不处理清结算，仍在处理中状态
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
        r=requests.post(host_pay+"/api/trade/bank_open/repay_webhook",data=json.dumps(data),headers=head_pay,verify=False)
        t=r.json()
        print(t)
    #cashFree还款模拟回调，注意：记得先要申请还款，调api,trade_fin_repay函数
    def cashFree_annon_event(self,loanNo):
        sql="select TRAN_ORDER_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330002' and TRAN_CHAN_NAME='cashFree支付服务商';"
        tran_order_no=DataBase(configs).get_one(sql)
        tran_order_no=tran_order_no[0]
        r=requests.post(host_pay+"/api/trade/cashFree/annon/event/"+tran_order_no,headers=head_pay,verify=False)
        t=r.json()
        print(t)
    #razorpay还款模拟回调，注意：记得先要申请还款，调api,trade_fin_repay函数
    def razorpay_annon_event_callback(self,loanNo,amount):
        sql="select TRAN_ORDER_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330002' and TRAN_CHAN_NAME='razorpayx';"
        tran_order_no=DataBase(configs).get_one(sql)
        tran_order_no=tran_order_no[0]
        data={"entity": "",
              "account_id": "",
              "event": "order.paid",
              "created_at": 0,
              "contains": [
                ""
              ],"payload": {
                "payment": {
                  "entity": {
                    "id": "",
                    "entity": "",
                    "amount":float(amount)*100,
                    "currency": "",
                    "status": "captured",
                    "order_id": tran_order_no,
                    "invoice_id": "",
                    "international": False,
                    "method": "",
                    "amount_refunded": 0,
                    "refund_status": "",
                    "captured": False,
                    "description": "",
                    "card_id": "",
                    "card": {
                      "id": "",
                      "entity": "",
                      "name": "",
                      "last4": "",
                      "network": "",
                      "type": "",
                      "issuer": "",
                      "international": False,
                      "emi": False
                    },
                    "bank": "",
                    "wallet": "",
                    "vpa": "",
                    "emi": {
                      "issuer": "",
                      "rate": "",
                      "duration": ""
                    },
                    "email": "",
                    "contact": "",
                    "fee": 0,
                    "tax": 0,
                    "error_code": "",
                    "error_description": "",
                    "created_at": 0,
                    "notes": {}
                  }
                },
                "order": {
                  "entity": {
                    "id": "",
                    "entity": "",
                    "amount": 0,
                    "amount_paid": 0,
                    "amount_due": 0,
                    "currency": "",
                    "receipt": "",
                    "offer_id": "",
                    "status": "",
                    "attempts": 0,
                    "created_at": 0,
                    "notes": {}
                  }
                },
                "refund": {
                  "entity": {
                    "id": "",
                    "entity": "",
                    "amount": 0,
                    "currency": "",
                    "payment_id": "",
                    "notes": {},
                    "receipt": "",
                    "acquirer_data": {
                      "arn": {},
                      "rrn": "",
                      "upi_transaction_id": ""
                    },
                    "created_at": 0
                  }
                },
                "transfer": {
                  "entity": {
                    "id": "",
                    "entity": "",
                    "source": "",
                    "recipient": "",
                    "amount": 0,
                    "currency": "",
                    "amount_reversed": 0,
                    "notes": {
                      "map": {}
                    },
                    "fees": 0,
                    "tax": 0,
                    "on_hold": "",
                    "on_hold_until": 0,
                    "recipient_settlement_id": "",
                    "created_at": 0,
                    "linked_account_notes": [
                      ""
                    ],
                    "processed_at": 0
                  }
                },
                "settlement": {
                  "entity": {
                    "id": "",
                    "entity": "",
                    "amount": 0,
                    "status": "",
                    "fees": 0,
                    "tax": 0,
                    "utr": "",
                    "created_at": 0
                  }
                }
              }
            }
        r=requests.post(host_pay+"/api/trade/razorpay/annon/event/callback",data=json.dumps(data),headers=head_pay_for_razorpay,verify=False)
        t=r.json()
        print(t)

    def payout_apply(self,loanNo,custNo):
        data = {
            "loanNo": loanNo,
            "custNo": custNo,
            "appNo": "102",
            "accType": "12010001"
        }
        r=requests.post("http://192.168.20.245:8083/api/fin/payout/apply",data=json.dumps(data),headers=head_pay_tmp)
        t=r.json()
        print(t)

if __name__ == '__main__':
    #payout_mock_apply('L1022203118190515132384870400','C1022203118190515003183529984')
    #cashFree_annon_event('L1022203098189733357668728832')
    #bank_open_annon_event('363636300062850024','11')
    payout_apply('L1042203318197808999085834240', 'C1042203318197808595446988800')
