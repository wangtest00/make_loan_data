import json,time
import requests
from database.dataBase_india import *
from public.check_api import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from data.var_tur import *

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

t=str(time.time()*1000000)[:10]
head_pay_for_razorpay={"Host":"test-pay.quantstack.in","Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
                "User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br","X-Razorpay-Event-Id":"HDSG"+t}

class DaiHou_tur():
    @hulue_error()
    def payout_mock_apply(self,loanNo,custNo,accType):
        data={
        "loanNo": loanNo,
        "custNo": custNo,
        "appNo": appNo,
        "accType": accType  # 12010001=银行卡，12010002=PayTm Wallet
    }
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
    #razorpay还款模拟回调，注意：必须有资金账户，记得先要申请还款，调api,trade_fin_repay函数
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
        print(r.url)
        t=r.json()
        print(t)
    #还款申请
    def re_payment_apply(self,loanNo,transAmt):
        sql="select CUST_NO,REPAY_DATE from lo_loan_dtl where LOAN_NO='"+loanNo+"';"
        m=DataBase(configs).get_one(sql)
        custNo=m[0]
        repayDate=m[1]
        data={
          "appNo": appNo,
          "loanNo": loanNo,
          "custNo": custNo,
          "instNum": 1,
          "repayDate": repayDate,
          "transAmt": transAmt,
          "custName": "wang mmmm shuang",
          "advance": "10000000",
          "isDefer": "10000000"
    }
        r=requests.post(host_pay+"/api/fin/re_payment/apply",data=json.dumps(data),headers=head_lixiang,verify=False)
        print(r.json())
    #paytm还款模拟回调
    def paytm_repay_webhook(self,loanNo,txnamount):
        sql = "select TRAN_FLOW_NO,TRAN_ORDER_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330002' and tran_stat='10220000';"
        sum2 = DataBase(configs).get_one(sql)
        tranFlowNo=sum2[0]
        tranorderno=sum2[1]
        print(sum2)
        data={
        "CURRENCY": "INR",
        "LINKDESCRIPTION": "Test Payment",
        "PAYMENTEMAILID": "ashurajput@icloud.com",
        "PAYMENTMOBILENUMBER": "9205994333",
        "GATEWAYNAME": "WALLET",
        "RESPMSG": "Txn Success",
        "BANKNAME": "WALLET",
        "PAYMENTMODE": "PPI",
        "CUSTID": "530484232",
        "MID": "NARAIN16906673626335",
        "MERC_UNQ_REF": "LI_"+tranorderno,
        "RESPCODE": "01",
        "TXNID": "20220413111212800110168193234977400",
        "TXNAMOUNT": txnamount,
        "ORDERID": tranFlowNo,
        "STATUS": "TXN_SUCCESS",
        "BANKTXNID": t,
        "TXNDATETIME": "2022-04-13 12:50:21.0",
        "TXNDATE": "2022-04-13",
        "MERCHANTLINKREFERENCEID": "81787160baf911ecb9389078412e4d89"
    }
        print(data)                                                 #表单格式提交,不转json
        r = requests.post(host_pay+"/api/trade/paytm/repay_webhook", data=data,verify=False)
        print(r.json())
    #处理还款中的订单为失效-若未还款成功（包括单边账和减免）则统一更新还款订单状态为失败
    def handle_repay(self):
        r=requests.post(host_pay+"/api/common/handle/re_pay?isAll=false&count=5000&minutes=5&loanNo=",verify=False)
        print("处理还款中的订单为失效接口响应=",r.json())


if __name__ == '__main__':
    data=['L1042205128212979749551800320',
'L1042205108212273275481554944',
'L1042205108212200351177310208',
'L1042205108212197657259737088',
'L1042205098211916418464284672',
'L1042205098211898798595833856',
'L1042205098211896376876007424',
'L1042205098211895369542598656',
'L1042205098211893001103015936',
'L1042205098211884102132105216',
'L1042204278207529786445332480',
'L1042204258206832969852321792',
'L1042204198204640821933441024',
'L1042204198204640535462477824',
'L1042204198204639908380475392',
'L1042204198204639612921118720',
'L1042204198204639323002437632',
'L1042204198204639006462509056',
'L1042204198204637449243262976',
'L1042204198204626754078441472',
'L1042204198204626463794855936',
'L1042204158203253824820019200',
'L1042204158203246179702734848',
'L1042204158203205809019224064',
'L1042204158203129040480174080',
'L1042204158203128516708073472',
'L1042204158203128243109429248',
'L1042204158203127981057703936',
'L1042204158203127443628949504',
'L1042204148202933615122907136',
'L1042204148202933305931399168',
'L1042204148202932697283362816',
'L1042204148202932394895015936',
'L1042204148202932095262326784',
'L1042204148202931789359153152',
'L1042204148202931479211343872',
'L1042204148202931170258911232',
'L1042204148202930843589738496',
'L1042204148202914420238778368',
'L1042204148202913015713169408',
'L1042204148202910839452401664',
'L1042204148202833679647703040',
'L1042204148202821491386155008',
'L1042203318197764717775880192',
'L1042203318197707694740799488',
'L1042203308197409456636755968',
'L1042203308197400707649961984',
'L1042203308197400181927510016',
'L1042203308197399820609191936',
'L1042203308197399598696955904',
'L1042203308197399075549806592',
'L1042203308197397330840977408',
'L1042203298197041619346849792',
'L1042203298197024965544050688',
'L1042203298196982788558356480',
'L1042203298196969032411447296',
'L1042203288196708865967063040',
'L1042203288196676154590167040',
'L1042203218194081137065394176',
'L1042203218194067629519077376',
'L1042203188192993974550724608',
'L1042203178192744595952697344',
'L1042203178192742756221911040',
'L1042203178192734146444066816',
'L1042203178192728527561490432',
'L1042104198072400980857389056',
'L1042104018065803775838846976']
    daihou=DaiHou_tur()
    for data in data:
        daihou.re_payment_apply(data,'4100')