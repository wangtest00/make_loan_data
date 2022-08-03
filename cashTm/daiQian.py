import datetime,random,string
from database.dataBase_india import *
from cashTm.daiHou import *
from data.var_cashTm import *
from common.api_Request import *
from common.commUrl_india import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class ApiTest(Api_Request):
    def __init__(self):
        self.apiTestName=Api_Request()
        #return self.apiTestName

class DaiQian_CashTm(ApiTest):
    def chaXunDaiQian(self,loanNo):
        sql1="select BEFORE_STAT from manage_need_loan.lo_loan_dtl where LOAN_NO='"+loanNo+"';"
        before_stat=DataBase(configs).get_one(sql1)
        before_stat=before_stat[0]
        return before_stat
    def lunXunDaiQian(self,loanNo):
        for t in range(1):
            before_stat=self.chaXunDaiQian(loanNo)
            if before_stat=='10260006':
                break
            else:
                time.sleep(3)
                print("贷前状态未变更为拒绝")
                continue
    #短信验证码，默认手机号后4位单个+5后取个位数，在逆序排列。注意非中国手机号
    def compute_code(self,m):
        m=m[-4:]
        x1=str(int(m[0])+5)
        x2=str(int(m[1])+5)
        x3=str(int(m[2])+5)
        x4=str(int(m[3])+5)
        x=x4[-1:]+x3[-1:]+x2[-1:]+x1[-1:]
        return x
    def head_token(self,token):
        head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","accept-encoding": "gzip","content-length": "0","host": "test-appa.quantstack.in",
              "content-type": "application/json;charset=utf-8","version_no":"2.6.3","app_type":"10090001",
            "x-app-type": "10090001","app_no": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
        return head
    def head_token_f(self,token):
        head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
              "content-type":"multipart/form-data; boundary=89795e05-6272-4b47-a620-b40b5a0ebcdc","version_no":"2.6.3","app_type":"10090001",
              "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
        return head
    def head_token_w(self,token):
        head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
              "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
              "content-type":"application/x-www-form-urlencoded","version_no":"2.6.3","app_type":"10090001",
              "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
        return head
    def login_code(self,registNo):
        code=self.compute_code(registNo)
        data={"appName":appName,"appNo":appNo,"appType":"10090001","code":code,"gaid":"12303937-ccde-46ee-a455-5146d36344dd","ipAddr":"192.168.20.223","osVersion":"10","phoneType":"HUAWEI",
              "registNo":registNo,"utmCampaign":"","utmContent":"","utmMedium":"","utmSource":"","utmTerm":"","versionNo":"2.6.3"}
        res=ApiTest.api_Request(self,'post', host_api+loginUrl,ApiTest.change_type(self,data),head_api)
        if res!=0:
            token=res['token']
            return token
        else:
            print('登录失败')
            return 0

    def cert_auth(self,registNo,headt):
        st=''
        for j in range(5):  #生成5个随机英文大写字母
            st+=random.choice(string.ascii_uppercase)
        num=str(random.randint(1000,9999))   #num+"4567"+num
        data = {"appName": appName, "appNo": appNo, "birthDay": "1991-05-06", "certNo": num + "4566" + num,
                "custFirstName": "wang", "custLastName": "shuang", "custMiddleName": "mmmm", "education": "10190006",
                "marriage": "10050001", "panNo": "" + st + num + "W", "registNo": registNo, "sex": "10030001",
                "useEmail": "sdfghhhj@gmail.com", "useLang": "90000001"}
        res=ApiTest.api_Request(self,'post',host_api+certAuthUrl,ApiTest.change_type(self,data),headt)
        if res!=0:
            m=json.loads(res['message'])#字符串转字典
            return m['custNo']
        else:
            pass
    def auth(self,registNo,custNo,headt):
        #第3个页面-家庭地址
        data1={"address":"wwsdddxx","county":"10010002","custNo":custNo,"postCode":"123456","residenceType":"10840005","state":"10010000"}
        r1=ApiTest.api_Request(self,'post',host_api+addressUrl,ApiTest.change_type(self,data1),headt)
        #第4个页面-工作认证1
        data2={"appNo":appNo,"certType":"WORK","custNo":custNo,"registNo":registNo}
        r2=ApiTest.api_Request(self,'post',host_api+singleAuthUrl,ApiTest.change_type(self,data2),headt)
        #第4个页面-工作认证2
        data3={"custNo":custNo,"employeeStatus":"10850002","monSalary":"10870009"}
        r3=ApiTest.api_Request(self,'post',host_api+workAuthUrl,ApiTest.change_type(self,data3),headt)
        #第5个页面-联系人认证
        data4=[{"contactName":"wang","custNo":custNo,"phoneNo":"6666677777","relation":"10110001"},{"contactName":"ye","custNo":custNo,"phoneNo":"7555566666","relation":"10110006"}]
        r4=ApiTest.api_Request(self,'post',host_api+contactAuthUrl,ApiTest.change_type(self,data4),headt)
    #申请提现
    def loan(self,registNo,custNo,headt):
        data={"appNo":appNo,"custNo":custNo,"registNo":registNo}
        t=ApiTest.api_Request(self,'post',host_api+withdrawUrl,ApiTest.change_type(self,data),headt)
        return t['loanNo']
    #更新kyc认证状态及其值
    def update_kyc_auth(self,registNo,custNo):
        t=str(time.time()*1000000)[:15]
        tnum1=str(random.randrange(10000,99999))
        tnum2=str(random.randrange(10000,99999))
        tnum3=str(random.randrange(10000,99999))
        tnum4=str(random.randrange(10000,99999))
        inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
        DataBase(configs).executeUpdateSql(sql)
        sql2="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '102', '10070015', '100700151627276671905.jpg', '100700151627276671905.jpg', '10080001', '.jpg', '918911', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700151627276671905.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        sql3="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '102', '10070016', '100700161627276676407.jpg', '100700161627276676407.jpg', '10080001', '.jpg', '581306', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700161627276676407.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        sql4="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '102', '10070017', '100700171627276682497.jpg', '100700171627276682497.jpg', '10080001', '.jpg', '569745', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700171627276682497.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        sql5="INSERT INTO `manage_need_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum4+"', '"+registNo+"', '"+custNo+"', '102', '10070004', '100700041627276687389.jpg', '100700041627276687389.jpg', '10080001', '.jpg', '575899', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700041627276687389.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        DataBase(configs).executeUpdateSql(sql2)
        DataBase(configs).executeUpdateSql(sql3)
        DataBase(configs).executeUpdateSql(sql4)
        DataBase(configs).executeUpdateSql(sql5)
    #绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱，写入cu_cust_beneficiary_account表     Razorpay渠道绑卡会掉创建资金账户接口https://test-pay.quantstack.in/api/trade/cust/create/contact/fund_account
    def bank_auth(self,custNo,headt):                            #Back_Account-12010001, （PayTm Wallet-12010002）
        bank_acct_no=str(random.randint(1000000000,9999999999))
        #bank_acct_no='53110884994'    #生产测试卡号
        data={"bankAcctName":"ashish rajput","bankAcctNo":bank_acct_no,"custNo":custNo,"ifscCode":"SCBL0036024","accType":"12010001","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r=ApiTest.api_Request(self,'post',host_api+bankAuthUrl,ApiTest.change_type(self,data),headt)
        data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"ashish rajput","accType":"12010001","ifscCode":"SCBL0036024","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r2=ApiTest.api_Request(self,'post',host_api+checkBankUrl,ApiTest.change_type(self,data2),headt)
        return bank_acct_no
    #暂时不使用，api调支付，支付会去请求创建资金账户-razorpay
    def create_contact_fund_account(self):
        #data={ "appNo":appNo,'bankAcctName': 'ashish rajput', 'bankNo': '53110884994', 'custNo': 'C1042204268207123079311327232', 'ifscCode': 'SCBL0036024', 'accType': '12010001', 'pageCode': '12000001', 'repeatBankAcctNo': '53110884994', "address": "123"}
        data={
          "appNo": appNo,
          "custNo": "C1042204268207123079311327232",
          "phoneNo": "9054856632",
          "acctNo": "53110884994",
          "acctName": "ashish rajput",
          "ifscCode": "SCBL0036024",
          "address": "123456"
    }
        r = ApiTest.api_Request(self,'post',host_pay +fundAccountUrl,ApiTest.change_type(self,data),headt)
        print(r)
    def bank_auth_paytm(self,custNo,headt):                            #PayTm Wallet-12010002（Back_Account-12010001）
        test_phoneNo = '7777777777'
        sql="DELETE from cu_cust_beneficiary_account where BENEFICIARY_NO='"+test_phoneNo+"';"
        DataBase(configs).executeUpdateSql(sql)
        bank_acct_no=test_phoneNo  #测试环境，卡号7777777777，目前能请求通三方,生产环境使用手机号和账户名：9205994333、Ashish rajput
        data={"bankAcctName":"Ashish rajput","bankAcctNo":bank_acct_no,"custNo":custNo,"accType":"12010002","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r=ApiTest.api_Request(self,'post',host_api+bankAuthUrl,ApiTest.change_type(self,data),headt)
        data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"wangmmmmshuang","accType":"12010002","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r2=ApiTest.api_Request(self,'post',host_api+checkBankUrl,ApiTest.change_type(self,data2),headt)
        return bank_acct_no
    #受益人账户接口
    def beneficiary_account(self,custNo,headt):
        data={"appNo":appNo,"custNo":custNo,"pageCode":"12000001"}  #受益账户配置-12000001
        r=ApiTest.api_Request(self,'post',host_api+beneficiaryAccountUrl,ApiTest.change_type(self,data),headt)
    #当前时间的前一天=跑批业务日期，才能正常申请借款
    def update_Batch_Log(self):
        sql='select now();'
        date_time=DataBase(configs).get_one(sql)
        d=str(date_time[0]+datetime.timedelta(days=-1))
        yudate=d[:4]+d[5:7]+d[8:10]
        sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
        BUSI_DATE=DataBase(configs).get_one(sql2)
        if yudate==BUSI_DATE[0]:
            print("当前服务器日期为:",date_time[0])
            print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
        else:
            sql3="update sys_batch_log set BUSI_DATE='"+yudate+"',BATCH_STAT='10490002',IS_PROD_SEL='10000001' where BUSI_DATE='"+BUSI_DATE[0]+"';"
            DataBase(configs).executeUpdateSql(sql3)
        DataBase(configs).closeDB()
    def trial_instalment(self,loanNo,headt):
        data={"loanNo":loanNo}
        t=ApiTest.api_Request(self,'post',host_api+instalmentUrl,data,headt)
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

    def withdraw(self,custNo,loanNo,headt,headw,accType):
        test_phoneNo = '7777777777'
        trial_list=self.trial_instalment(loanNo,headw)
        if trial_list==0:
            print("未获取到期数和贷款金额,不调提现接口")
        else:
            sql = "delete from pay_tran_dtl where IN_ACCT_NO='"+test_phoneNo+"';"  # 支付要查重复
            DataBase(configs).executeUpdateSql(sql)
            instNum=trial_list[0]
            loanAmt=trial_list[1]
            data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loanNo,"prodNo":prodNo,"accType":accType}
            r=ApiTest.api_Request(self,'post',host_api+confirmWithdrawUrl,ApiTest.change_type(self,data),headt)

    def payout_for_razorpay(self,cust_no,bank_no):
        sql1="DELETE  from pay_cust_found_info where CUST_NO='"+cust_no+"';"
        DataBase(configs).executeUpdateSql(sql1)
        #注意卡号需要与cu_cust_bank_card_dtl表中卡号保持一致
        t=str(time.time()*1000000)[:15]
        inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql='''INSERT INTO `pay_cust_found_info`(`ID`, `CUST_NO`, `APP_NO`, `MERCHANT_NO`, `FUND_ACCOUNT_ID`, `CONTACT_ID`, `CUST_NAME`, `BANK_NAME`, `IFSC`, `BANK_NO`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`)
    VALUES ("'''+t+'''", "'''+cust_no+'''", "'''+appNo+'''", "'''+appName+'''RazorpayTest_Payout", "'''+cust_no+'''", NULL, 'wang test api', 'shuang', 'HDFC0003740', "'''+bank_no+'''", NULL, "'''+inst_time+'''", "'''+cust_no+'''", NULL, NULL);'''
        DataBase(configs).executeUpdateSql(sql)

    #测试前，需要检查app信息支付渠道配置是否已配置razorpay、bankopen、cashfree
    #登录后，api调支付去申请还款,需要检查pay_tran_dtl表数据及状态
    def trade_fin_repay(self,loanNo):
        sql='''select b.REGIST_NO,b.CUST_NO,a.REPAY_DATE,a.RECEIVE_AMT from fin_ad_dtl a left join lo_loan_cust_rel b on a.LOAN_NO=b.loan_no
    where a.LOAN_NO="'''+loanNo+'''" ;'''
        repay_list=DataBase(configs).get_one(sql)
        print(repay_list)
        token=login_code(repay_list[0])
        headt=head_token(token)
        data={"advance":"10000000","custNo":repay_list[1],"loanNo":loanNo,"repayDate":repay_list[2],"repayInstNum":1,"tranAppType":"10090001","transAmt":str(repay_list[3])}
        t=ApiTest.api_Request(self,'post',host_api+repayUrl,ApiTest.change_type(self,data),headt)
        print(t)
    #razorpayx放款模拟回调，注意：记得先要申请放款,测试环境不验证签名
    def razorpayx_annon_event_callback(self,loanNo):
        sql="select TRAN_ORDER_NO,ACT_TRAN_AMT from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330001' and TRAN_CHAN_NAME='razorpayx';"
        tran=DataBase(configs).get_one(sql)
        tran_order_no=tran[0]
        amount=tran[1]
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
            "lanaDigital": 0,
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
            "lanaDigital": 0,
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
        t=ApiTest.api_Request(self,'post',host_pay+raorpayCallbackUrl,ApiTest.change_type(self,data),head_pay_for_razorpay)
        print('razorpay模拟放款回调，响应=',t)
    #放款申请
    def payout_apply_test(self,loanNo):
        sql = "select CUST_NO,REPAY_DATE from lo_loan_dtl where LOAN_NO='"+loanNo+"';"
        m = DataBase(configs).get_one(sql)
        custNo = m[0]
        data={
          "loanNo": loanNo,
          "custNo": custNo,
          "appNo": appNo,
          "accType": "12010001"}  #注意这里区分类型，银行卡或paytm
        r=ApiTest.api_Request(self,'post',host_pay+'/api/fin/payout/apply',ApiTest.change_type(self,data),head_lixiang)
        print(r)
    #放款模拟回调
    def paytm_payout_webhook(self,loanNo,status):
        t0 = str(time.time() * 1000000)
        sql="select ACT_TRAN_AMT,TRAN_FLOW_NO from pay_tran_dtl where LOAN_NO='"+loanNo+"' and TRAN_USE='10330001' and (tran_stat='10220004' or tran_stat='10220001' or tran_stat='10220003');"
        sum=DataBase(configs).get_one(sql)
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
        "status": status,
        #"status": "FAILURE",#模拟提现失败
        "statusCode": "DE_001",
        "statusMessage": "Successful disbursal to Wallet is done"
    }
        r=ApiTest.api_Request(self,'post',host_pay+paytmWebhookUrl,ApiTest.change_type(self,data),head_pay)
    #插入白名单
    def insert_white_list(self,registNo):
        t =str(time.time() * 1000000)[:15]
        inst_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql='''INSERT INTO `manage_need_loan`.`cu_white_list_dtl`(`ID`, `WHITE_LIST_TYPE`, `WHITE_LIST_VALUE`, `APP_NO`, `RISK_SCORE`, `USEABLE`, `VALID_START_DATE`, `VALID_END_DATE`, `ORIGIN`, `DESCRIPTION`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) 
        VALUES ("'''+t+'''", '10140001', "'''+registNo+'''", "'''+appNo+'''", "'''+prodNo+'''", '10000001', '20220415', '20220715', 'auto_test', NULL, NULL, "'''+inst_time+'''", 'wangs@whalekun.com', "'''+inst_time+'''", 'wangs@whalekun.com');'''
        DataBase(configs).executeUpdateSql(sql)

    def cx_pay_chan_service(self):
        sql="select PAY_CHAN_SERVICE from sys_app_info where APP_NO='"+appNo+"';"
        pay_chan_service=DataBase(configs).get_one(sql)
        pay_chan_service=pay_chan_service[0]
        #print(pay_chan_service)
        return pay_chan_service
    def app_version(self):
        data={"appNo": "102", "appType": "10090001", "versionNo": "2.6.8", "versionValue": "268"}
        #r=ApiTest.api_Request(self,'post',host_api+appVersionUrl,ApiTest.change_type(self,data),head_api)
        r=ApiTest.api_Request(self,'post',host_api+appVersionUrl,ApiTest.change_type(self,data),head_api)

if __name__ == '__main__':
    registNo='8832701318'
    # loanNo = 'L1042205278218431170053079040'
    # token=DaiQian_Tur().login_code(registNo)
    # headt = DaiQian_Tur().head_token(token)
