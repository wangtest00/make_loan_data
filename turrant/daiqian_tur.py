import datetime
import random
import string
from database.dataBase_tur import *
from turrant.daihou_tur import *
from data.var_tur import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
t0=str(time.time()*1000000)

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def check_api(r):
    if r.status_code==200:
        t=r.json()
        if t['hasRegistration'] is False:
            print("校验成功，接口返回=",t)
            return t
        else:
            print("校验失败，接口返回=",t)
            return 0
    else:
        print("环境可能不稳定，接口返回=",r.content)
        return 0

#短信验证码，默认手机号后4位单个+5后取个位数，在逆序排列。注意非中国手机号
def compute_code(m):
    m=m[-4:]
    x1=str(int(m[0])+5)
    x2=str(int(m[1])+5)
    x3=str(int(m[2])+5)
    x4=str(int(m[3])+5)
    x=x4[-1:]+x3[-1:]+x2[-1:]+x1[-1:]
    return x
def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","accept-encoding": "gzip","content-length": "0","host": "test-appa.quantstack.in",
          "content-type": "application/json;charset=utf-8","version_no":"1.0.0","app_type":"10090001",
        "x-app-type": "10090001","app_no": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
    return head
def head_token_f(token):
    head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
          "content-type":"multipart/form-data; boundary=89795e05-6272-4b47-a620-b40b5a0ebcdc","version_no":"1.0.0","app_type":"10090001",
          "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def head_token_w(token):
    head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
          "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
          "content-type":"application/x-www-form-urlencoded","version_no":"1.0.0","app_type":"10090001",
          "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def login_code(registNo):
    code=compute_code(registNo)
    data={"appName":appName,"appNo":appNo,"appType":"10090001","code":code,"gaid":"12303937-ccde-46ee-a455-5146d36344dd","ipAddr":"192.168.20.223","osVersion":"10","phoneType":"HUAWEI",
          "registNo":registNo,"utmCampaign":"","utmContent":"","utmMedium":"","utmSource":"","utmTerm":"","versionNo":"1.0.0"}
    r=requests.post(host_api+"/api/cust_info/cust/login?lang=en",data=json.dumps(data),headers=head_api,verify=False)
    c=r.json()
    print(c)
    if c!=0:
        token=c['token']
        return token
    else:
        return 0

def cert_auth(registNo,headt):
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num=str(random.randint(1000,9999))
    data={"appName":appName,"appNo":appNo,"birthDay":"1999-05-06","certNo":num+"4566"+num,"custFirstName":"wang","custLastName":"shuang","custMiddleName":"mmmm","education":"10190006",
          "marriage":"10050001","panNo":""+st+num+"W","registNo":registNo,"sex":"10030001","useEmail":"sdfghhhj@gmail.com","useLang":"90000001"}
    r=requests.post(host_api+'/api/cust_india/cert/cert_auth?lang=en',data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)
    if t!=0:
        m=json.loads(t['message'])#字符串转字典
        return m['custNo']
    else:
        pass
def auth(registNo,custNo,headt):
    #第3个页面-家庭地址
    data1={"address":"wwsdddxx","county":"10010002","custNo":custNo,"postCode":"123456","residenceType":"10840005","state":"10010000"}
    r1=requests.post(host_api+'/api/cust_india/cert/save_address?lang=en',data=json.dumps(data1),headers=headt,verify=False)
    print(r1.json())
    #第4个页面-工作认证1
    data2={"appNo":appNo,"certType":"WORK","custNo":custNo,"registNo":registNo}
    r2=requests.post(host_api+'/api/cust_india/query/single_cust_auth?lang=en',data=json.dumps(data2),headers=headt,verify=False)
    print(r2.json())
    #第4个页面-工作认证2
    data3={"custNo":custNo,"employeeStatus":"10850002","monSalary":"10870009"}
    r3=requests.post(host_api+'/api/cust_india/work/auth?lang=en',data=json.dumps(data3),headers=headt,verify=False)
    print(r3.json())
    #第5个页面-联系人认证
    data4=[{"contactName":"wang","custNo":custNo,"phoneNo":"6666677777","relation":"10110001"},{"contactName":"ye","custNo":custNo,"phoneNo":"7555566666","relation":"10110006"}]
    r4=requests.post(host_api+'/api/cust_india/contact/auth?lang=en',data=json.dumps(data4),headers=headt,verify=False)
    print(r4.json())
#申请提现
def loan(registNo,custNo,headt):
    data={"appNo":appNo,"custNo":custNo,"registNo":registNo}
    r=requests.post(host_api+'/api/loan_india/start?lang=en',data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)
    return t['loanNo']

#更新kyc认证状态及其值
def update_kyc_auth(registNo,custNo):
    t=str(time.time()*1000000)[:15]
    tnum1=str(random.randrange(10000,99999))
    tnum2=str(random.randrange(10000,99999))
    tnum3=str(random.randrange(10000,99999))
    tnum4=str(random.randrange(10000,99999))
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
    DataBase(inter_db).executeUpdateSql(sql)
    sql2="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '102', '10070015', '100700151627276671905.jpg', '100700151627276671905.jpg', '10080001', '.jpg', '918911', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700151627276671905.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '102', '10070016', '100700161627276676407.jpg', '100700161627276676407.jpg', '10080001', '.jpg', '581306', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700161627276676407.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '102', '10070017', '100700171627276682497.jpg', '100700171627276682497.jpg', '10080001', '.jpg', '569745', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700171627276682497.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql5="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum4+"', '"+registNo+"', '"+custNo+"', '102', '10070004', '100700041627276687389.jpg', '100700041627276687389.jpg', '10080001', '.jpg', '575899', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700041627276687389.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(inter_db).executeUpdateSql(sql2)
    DataBase(inter_db).executeUpdateSql(sql3)
    DataBase(inter_db).executeUpdateSql(sql4)
    DataBase(inter_db).executeUpdateSql(sql5)
#绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱，写入cu_cust_beneficiary_account表
def bank_auth(custNo,headt):                            #Back_Account-12010001, （PayTm Wallet-12010002）
    bank_acct_no=str(random.randint(100000000,999999999))
    data={"bankAcctName":"wangmmmmshuang","bankAcctNo":bank_acct_no,"custNo":custNo,"ifscCode":"SBIN0001537","accType":"12010001","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
    print(data)
    r=requests.post(host_api+'/api/cust_india/bank/bank_auth?lang=en',data=json.dumps(data),headers=headt,verify=False)
    print("绑卡认证接口响应=",r.json())
    data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"wangmmmmshuang","accType":"12010001","ifscCode":"SBIN0001537","pageCode":"12000001","reBankAcctNo":bank_acct_no}
    # print(data2)
    # r2=requests.post(host_api+'/api/cust_india/bank/checkBankCard?lang=en',data=json.dumps(data2),headers=headt,verify=False)
    # print("校验银行卡接口响应=",r2.json())
    return bank_acct_no

test_phoneNo='7777777777'
def bank_auth_paytm(custNo,headt):                            #PayTm Wallet-12010002（Back_Account-12010001）
    sql="DELETE from cu_cust_beneficiary_account where BENEFICIARY_NO='"+test_phoneNo+"';"
    DataBase(inter_db).executeUpdateSql(sql)
    bank_acct_no=test_phoneNo  #测试环境，卡号7777777777，目前能请求通三方,生产环境使用手机号和账户名：9205994333、Ashish rajput
    data={"bankAcctName":"Ashish rajput","bankAcctNo":bank_acct_no,"custNo":custNo,"accType":"12010002","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
    print(data)
    r=requests.post(host_api+'/api/cust_india/bank/bank_auth?lang=en',data=json.dumps(data),headers=headt,verify=False)
    print("绑卡认证接口响应=",r.json())
    data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"wangmmmmshuang","accType":"12010002","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
    r2=requests.post(host_api+'/api/cust_india/bank/checkBankCard?lang=en',data=json.dumps(data2),headers=headt,verify=False)
    print("校验银行卡接口响应=",r2.json())
    return bank_acct_no
#受益人账户接口
def beneficiary_account(custNo,headt):
    data={"appNo":appNo,"custNo":custNo,"pageCode":"12000001"}  #受益账户配置-12000001
    r=requests.post(host_api+"/api/compile/cust_beneficiary_account?lang=en",data=json.dumps(data),headers=headt,verify=False)
    print('受益人账户接口响应=',r.json())

#当前时间的前一天=跑批业务日期，才能正常申请借款
def update_Batch_Log():
    sql='select now();'
    date_time=DataBase(inter_db).get_one(sql)
    d=str(date_time[0]+datetime.timedelta(days=-1))
    yudate=d[:4]+d[5:7]+d[8:10]
    sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
    BUSI_DATE=DataBase(inter_db).get_one(sql2)
    if yudate==BUSI_DATE[0]:
        print("当前服务器日期为:",date_time[0])
        print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
    else:
        sql3="update sys_batch_log set BUSI_DATE='"+yudate+"',BATCH_STAT='10490002',IS_PROD_SEL='10000001' where BUSI_DATE='"+BUSI_DATE[0]+"';"
        DataBase(inter_db).executeUpdateSql(sql3)
    DataBase(inter_db).closeDB()

def trial_instalment(loanNo,headt):
    data={"loanNo":loanNo}
    r=requests.post(host_api+"/api/loan_info/trial/instalment?lang=en",data=data,headers=headt,verify=False)
    t=r.json()
    #print(t)
    list=[]
    if t['single'] is True:
        loanInstNums=str(t['loanInstNums'])
        loanAmount=t['loanAmount']
        list.append(loanInstNums)
        list.append(loanAmount)
        print("期数，贷款金额=",list)
        return list
    else:
        print("试算接口未获取到数据")
        return 0

def withdraw(custNo,loanNo,headt,headw,accType):
    trial_list=trial_instalment(loanNo,headw)
    if trial_list==0:
        print("未获取到期数和贷款金额,不调提现接口")
    else:
        sql = "delete from pay_tran_dtl where IN_ACCT_NO='"+test_phoneNo+"';"  # 支付要查重复
        DataBase(inter_db).executeUpdateSql(sql)
        instNum=trial_list[0]
        loanAmt=trial_list[1]
        data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loanNo,"prodNo":prodNo,"accType":accType}
        r=requests.post(host_api+"/api/trade/fin/less/withdraw?lang=en",data=json.dumps(data),headers=headt,verify=False)
        print("api申请放款接口响应=",r.json())


def payout_for_razorpay(cust_no,bank_no):
    sql1="DELETE  from pay_cust_found_info where CUST_NO='"+cust_no+"';"
    DataBase(inter_db).executeUpdateSql(sql1)
    #注意卡号需要与cu_cust_bank_card_dtl表中卡号保持一致
    t=str(time.time()*1000000)[:15]
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql='''INSERT INTO `pay_cust_found_info`(`ID`, `CUST_NO`, `APP_NO`, `MERCHANT_NO`, `FUND_ACCOUNT_ID`, `CONTACT_ID`, `CUST_NAME`, `BANK_NAME`, `IFSC`, `BANK_NO`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`)
VALUES ("'''+t+'''", "'''+cust_no+'''", "'''+appNo+'''", "'''+appName+'''RazorpayTest_Payout", "'''+cust_no+'''", NULL, 'wang test api', 'shuang', 'HDFC0003740', "'''+bank_no+'''", NULL, "'''+inst_time+'''", "'''+cust_no+'''", NULL, NULL);'''
    DataBase(inter_db).executeUpdateSql(sql)

#测试前，需要检查app信息支付渠道配置是否已配置razorpay、bankopen、cashfree
#登录后，api调支付去申请还款,需要检查pay_tran_dtl表数据及状态
def trade_fin_repay(loanNo):
    sql='''select b.REGIST_NO,b.CUST_NO,a.REPAY_DATE,a.RECEIVE_AMT from fin_ad_dtl a left join lo_loan_cust_rel b on a.LOAN_NO=b.loan_no
where a.LOAN_NO="'''+loanNo+'''" ;'''
    repay_list=DataBase(inter_db).get_one(sql)
    print(repay_list)
    token=login_code(repay_list[0])
    headt=head_token(token)
    data={"advance":"10000000","custNo":repay_list[1],"loanNo":loanNo,"repayDate":repay_list[2],"repayInstNum":1,"tranAppType":"10090001","transAmt":str(repay_list[3])}
    r=requests.post(host_api+"/api/trade/fin/repay?lang=en",data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)

t=str(time.time()*1000000)[:10]
head_pay_for_razorpayx={"Host":"test-pay.quantstack.in","Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
"User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br","X-Razorpay-Event-Id":"PAYOUT"+t,"X-Razorpay-Signature":"123456"}


#razorpayx放款模拟回调，注意：记得先要申请放款,测试环境不验证签名
def razorpayx_annon_event_callback(loanNo,amount):
    sql="select TRAN_ORDER_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330001' and TRAN_CHAN_NAME='razorpayx';"
    tran_order_no=DataBase(inter_db).get_one(sql)
    tran_order_no=tran_order_no[0]
    data={"entity": "",
  "account_id": "",
  "event": "payout.processed",
  "created_at": 0,
  "contains": [
    ""
  ],
  "payload": {
    "payout": {
      "entity": {
        "id": tran_order_no,
        "entity": "",
        "account_number": "",
        "fund_account_id": "",
        "amount": float(amount)*100,
        "currency": "",
        "credit": 0,
        "debit": 0,
        "balance": 0,
        "notes": {},
        "fees": 0,
        "tax": 0,
        "status": "",
        "purpose": "",
        "utr": "",
        "mode": "",
        "reference_id": {},
        "narration": "",
        "batch_id": {},
        "failure_reason": "",
        "created_at": 0
      }
    },
    "transaction": {
      "entity": {
        "id": "",
        "entity": "",
        "account_number": "",
        "amount": 0,
        "currency": "",
        "credit": 0,
        "debit": 0,
        "balance": 0,
        "source": {
          "id": "",
          "entity": "",
          "fund_account_id": "",
          "amount": 0,
          "notes": {},
          "fees": 0,
          "tax": 0,
          "status": "",
          "utr": "",
          "mode": "",
          "created_at": 0
        }
      }
    }
  }
}
    r=requests.post(host_pay+"/api/trade/razorpay_x/annon/event/callback",data=json.dumps(data),headers=head_pay_for_razorpayx,verify=False)
    t=r.json()
    print(t)
#放款申请
def payout_apply_test(loanNo):
    sql = "select CUST_NO,REPAY_DATE from lo_loan_dtl where LOAN_NO='"+loanNo+"';"
    m = DataBase(inter_db).get_one(sql)
    custNo = m[0]
    data={
      "loanNo": loanNo,
      "custNo": custNo,
      "appNo": appNo,
      "accType": "12010001"}  #注意这里暂时写死为paytm类型
    r=requests.post(host_pay+'/api/fin/payout/apply',data=json.dumps(data),headers=head_pay,verify=False)
    print(r.json())
#放款模拟回调
def paytm_payout_webhook(loanNo):
    sql="select ACT_TRAN_AMT,TRAN_FLOW_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330001' and (tran_stat='10220004' or tran_stat='10220001' or tran_stat='10220003');"
    sum=DataBase(inter_db).get_one(sql)
    orderId=sum[1]
    amount=float(sum[0])
    data={
    "result": {
        "amount": str(amount),
        "beneficiaryIfsc": None,
        "beneficiaryName": "wangmmmmshuang",
        "cachedTime": None,
        "commissionAmount": "0.00",
        "createdOn": "13-04-2022 08:05:09",
        "isCachedData": None,
        "mid": "NARAIN39025689320637",
        "nextRetryTime": "13-04-2022 08:10:13",
        "orderId": orderId,
        "paytmOrderId": t0,
        "processedOn": "13-04-2022 08:05:13",
        "remitterName": "NARAINSONS INVESTMENTS FINANCE AND CONSULTANCY",
        "retryCount": None,
        "reversalReason": None,
        "rrn": "39885896709",
        "scheduleOn": None,
        "tax": "0.00"
    },
    "status": "SUCCESS",
    "statusCode": "DE_001",
    "statusMessage": "Successful disbursal to Wallet is done"
}
    print(data)
    r=requests.post(host_pay+"/api/trade/paytm/payout_webhook",data=json.dumps(data),headers=head_pay,verify=False)
    print(r.json())

def insert_white_list(registNo):
    t =str(time.time() * 1000000)[:15]
    inst_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql='''INSERT INTO `manage_need_loan`.`cu_white_list_dtl`(`ID`, `WHITE_LIST_TYPE`, `WHITE_LIST_VALUE`, `APP_NO`, `RISK_SCORE`, `USEABLE`, `VALID_START_DATE`, `VALID_END_DATE`, `ORIGIN`, `DESCRIPTION`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) 
    VALUES ("'''+t0[:-2]+'''", '10140001', "'''+registNo+'''", "'''+appNo+'''", "'''+prodNo+'''", '10000001', '20220415', '20220715', 'auto_test', NULL, NULL, "'''+inst_time+'''", 'wangs@whalekun.com', "'''+inst_time+'''", 'wangs@whalekun.com');'''
    DataBase(inter_db).executeUpdateSql(sql)

if __name__ == '__main__':
    # registNo='8378994636'
    # token=login_code(registNo)
    # headt=head_token(token)
    registNo = '8215602929'
    token = login_code(registNo)
    headt = head_token(token)
    # headw = head_token_w(token)
    custNo = 'C1042204258206759260848324608'
    loanNo = 'L1042204258206759386941685760'
    #bank_auth_paytm(custNo, headt)
    # #payout_for_razorpay(custNo, '123123')
    #withdraw( custNo, loanNo, headt, headw,'12010002')
    #payout_apply_test('L1042204158203142570617012224')
    #paytm_payout_webhook('L1042204158203255911347847168')
    bank_auth(custNo, headt)
    #payout_apply_test(loanNo)