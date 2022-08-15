import datetime,random,string
from database.dataBase_india import *
from turrant.daiHou import *
from data.var_tur import *
from common.api_Request import *
from common.commUrl_india import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class ApiTest(Api_Request):
    def __init__(self):
        self.apiTestName=Api_Request()
        #return self.apiTestName

class DaiQian_Tur(ApiTest):
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
              "content-type": "application/json;charset=utf-8","version_no":"1.0.0","app_type":"10090001",
            "x-app-type": "10090001","app_no": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
        return head
    def head_token_f(self,token):
        head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
              "content-type":"multipart/form-data; boundary=89795e05-6272-4b47-a620-b40b5a0ebcdc","version_no":"1.0.0","app_type":"10090001",
              "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
        return head
    def head_token_w(self,token):
        head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
              "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":"test-appa.quantstack.in",
              "content-type":"application/x-www-form-urlencoded","version_no":"1.0.0","app_type":"10090001",
              "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
        return head
    def login_code(self,registNo):
        code=self.compute_code(registNo)
        data={"appName":appName,"appNo":appNo,"appType":"10090001","code":code,"gaid":"12303937-ccde-46ee-a455-5146d36344dd","ipAddr":"192.168.20.223","osVersion":"10","phoneType":"HUAWEI",
              "registNo":registNo,"utmCampaign":"","utmContent":"","utmMedium":"","utmSource":"","utmTerm":"","versionNo":"1.0.0"}
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
        num=str(random.randint(1000,9999))   #certNo=num+"4567"+num
        data={"appName":appName,"appNo":appNo,"birthDay":"1998-06-06","certNo":num+"1122"+num,"custFirstName":"wang","custLastName":"shuang","custMiddleName":"mmmm","education":"10190006",
              "marriage":"10050001","panNo":""+st+num+"W","registNo":registNo,"sex":"10030001","useEmail":"sdfghhhj@gmail.com","useLang":"90000001"}
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
    #绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱，写入cu_cust_beneficiary_account表
    #Razorpay渠道绑卡会调创建资金账户接口https://test-pay.quantstack.in/api/trade/cust/create/contact/fund_account
    def bank_auth(self,custNo,headt):                            #Back_Account-12010001, （PayTm Wallet-12010002）
        bank_acct_no=str(random.randint(1000000000,9999999999))
        #bank_acct_no='53110884994'    #生产测试卡号
        data={"bankAcctName":"ashish rajput","bankAcctNo":bank_acct_no,"custNo":custNo,"ifscCode":"SCBL0036024","accType":"12010001","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r=ApiTest.api_Request(self,'post',host_api+bankAuthUrl,ApiTest.change_type(self,data),headt)
        data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"ashish rajput","accType":"12010001","ifscCode":"SCBL0036024","pageCode":"12000001","reBankAcctNo":bank_acct_no}
        r2=ApiTest.api_Request(self,'post',host_api+checkBankUrl,ApiTest.change_type(self,data2),headt)
        return bank_acct_no
    #暂时不使用，api调支付，支付会调用该接口去请求创建资金账户-razorpay
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
        print("绑卡认证接口响应=",r)
        data2={"custNo":custNo,"bankAcctNo":bank_acct_no,"bankAcctName":"wangmmmmshuang","accType":"12010002","pageCode":"12000001","repeatBankAcctNo":bank_acct_no}
        r2=ApiTest.api_Request(self,'post',host_api+checkBankUrl,ApiTest.change_type(self,data2),headt)
        print("校验银行卡接口响应=",r2)
        return bank_acct_no
    #受益人账户接口
    def beneficiary_account(self,custNo,headt):
        data={"appNo":appNo,"custNo":custNo,"pageCode":"12000001"}  #受益账户配置-12000001
        r=ApiTest.api_Request(self,'post',host_api+beneficiaryAccountUrl,ApiTest.change_type(self,data),headt)
        print('受益人账户接口响应=',r)
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
    #插入资金账户数据
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
        if repay_list is None:
            pass
        else:
            token=self.login_code(repay_list[0])
            headt=self.head_token(token)
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
    #支付放款申请
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
    #paytm放款模拟回调
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
    #新客抓取数据，1.授权后，登录注册成功后在首页抓取，当时未认证
    def xinke_grab_data(self,registNo,headt):
        timev = str(time.time() * 1000000)[:13]
        data1={"appNo":appNo,"busiType":"10070021","certNo":"","deviceInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","ipAddress":"192.168.20.139","ipResolveCit":"Intranet IP","ipResolveCom":"Intranet IP","mac":"please open wifi","mobileBrand":"OPPO","mobileModel":"CPH1937","otherInfo":"Android版本API:--30--设备唯一id:acd394f8ac0cc545--厂商分配的序列号:unknown","phoneNo":registNo,"recordBehavior":"Capture device data","recordTime":timev,"systemVersion":"11","userId":""},"grabType":"runtime","registNo":registNo}
        data2={"appNo":appNo,"behaviorCode":"11000001","custNo":"","loanNo":"","msgInfo":[{"address":"QP-131214","body":"Too much to manage on a limited budget, Harsh? Don't worry. Complete your CASHe loan application on your smartphone. Click weurl.co/dmL23Q. *T&C - CASHe","date":timev,"date_sent":1618720040,"id":998,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Save Rs 350 + only 4 hours installation specially for you! Get Airtel Digital TV HD Box at just Rs 1650 now. Click i.airtel.in/bhdthppr","date":timev,"date_sent":1462007040,"id":997,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Get high quality security cameras that capture clear videos even at night! Introducing Airtel Xsafe, an advanced security camera solution with Night vision for maximum efficiency. Book now! i.airtel.in/e/XSafe","date":1655024002777,"date_sent":1461263040,"id":996,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"AD-AIRBIL","body":"Hi! Bill of Rs 4506 is due for payment on 14-JUN-22 for your Airtel No. 7428089716. Pay with ease from the comfort of your home using Airtel Thanks App https://i.airtel.in/PPpayBills or website www.airtel.in. Ignore if already paid","date":1655016300668,"date_sent":1453558040,"id":995,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"JD-CashTM","body":"CashTM: Dear customer, your OTP  is  1794. Please do not share it with anyone else.","date":1654953784617,"date_sent":1391048040,"id":994,"person":0,"read":0,"seen":1,"status":-1,"type":1}],"registNo":registNo,"remark":"复客直接在首页进件抓取"}
        data3={"appNo":appNo,"busiType":"10070023","certNo":"","contacts":[{"contactName":"Advance Talktime, 😁😁😁😁😆","contactNo":"52141","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":timev,"userId":""},{"contactName":"aEhrKh","contactNo":"3263124996","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922012,"userId":""},{"contactName":"af25DX","contactNo":"6782386824","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922134,"userId":""},{"contactName":"AfsJPR","contactNo":"9947615725","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922249,"userId":""},{"contactName":"Ah0SVk","contactNo":"7337371118","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922388,"userId":""},{"contactName":"ahaAm7","contactNo":"7477647591","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922522,"userId":""},{"contactName":"Airtel Money@*&$%✓😛","contactNo":"*400#","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922693,"userId":""},{"contactName":"ajEK0W","contactNo":"7554005234","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922847,"userId":""},{"contactName":"AkyRMo","contactNo":"3473860188","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923024,"userId":""},{"contactName":"Ambulance*;:%@#\"","contactNo":"102","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923136,"userId":""}],"grabType":"runtime","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        data4={"appNo":appNo,"busiType":"10070022","certNo":"","gpsInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","latitude":"104.0638612","longitude":"30.5457533","mac":"please open wifi","recordBehavior":"11000002","recordTime":timev,"userId":""},"grabType":"runtime","registNo":registNo}
        data5={"appNo":appNo,"apps":[{"appName":"MOMO","appPackage":"com.moneed.wallet","appVersionNo":"10059","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1625649657726","lastUpdateTime":"1635414878292","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926300,"userId":""},{"appName":"飞鸽传书","appPackage":"com.netfeige","appVersionNo":"50","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1609124888508","lastUpdateTime":"1609124888508","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926316,"userId":""},{"appName":"Gboard","appPackage":"com.google.android.inputmethod.latin","appVersionNo":"67384622","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121035000","lastUpdateTime":"1638151939487","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926324,"userId":""},{"appName":"COTA更新","appPackage":"com.oppo.cota","appVersionNo":"2030021","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1627988864000","lastUpdateTime":"1645702910000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926349,"userId":""},{"appName":"OppoLFEHer","appPackage":"com.oppo.lfeh","appVersionNo":"1002","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121026000","lastUpdateTime":"1645718606000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Circular","appPackage":"com.android.theme.icon_pack.circular.android","appVersionNo":"1","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606120991000","lastUpdateTime":"1645718565000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Android 设置向导","appPackage":"com.google.android.apps.restore","appVersionNo":"9568","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121045000","lastUpdateTime":"1645702824000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926380,"userId":""}],"busiType":"10070012","certNo":"","grabType":"runtime","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_device_info?lang=en',ApiTest.change_type(self,data1),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_msg_data?lang=en',ApiTest.change_type(self,data2),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_contact?lang=en',ApiTest.change_type(self,data3),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_gps_info?lang=en',ApiTest.change_type(self,data4),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_application_data?lang=en',ApiTest.change_type(self,data5),headt)
    def xinke_jinjian_grab_data(self,registNo,headt):
        sql="select a.CUST_NO,a.CERT_NO from cu_cust_cert_sensitive_dtl a left join cu_cust_reg_dtl b on a.CUST_NO=b.CUST_NO where b.REGIST_NO='"+registNo+"';"
        data = DataBase(configs).get_one(sql)
        custNo=data[0]
        certNo=data[1]
        timev = str(time.time() * 1000000)[:13]
        data1={"appNo":appNo,"busiNo":custNo,"busiType":"10070021","certNo":certNo,"deviceInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","ipAddress":"192.168.20.139","ipResolveCit":"Intranet IP","ipResolveCom":"Intranet IP","mac":"please open wifi","mobileBrand":"OPPO","mobileModel":"CPH1937","otherInfo":"Android版本API:--30--设备唯一id:acd394f8ac0cc545--厂商分配的序列号:unknown","phoneNo":registNo,"recordBehavior":"Incoming grab","recordTime":1655357382909,"systemVersion":"11","userId":custNo},"grabType":"loanStart","registNo":registNo}
        data2={"appNo":appNo,"behaviorCode":"11000003","custNo":certNo,"loanNo":"","msgInfo":[{"address":"QP-131214","body":"Too much to manage on a limited budget, Harsh? Don't worry. Complete your CASHe loan application on your smartphone. Click weurl.co/dmL23Q. *T&C - CASHe","date":timev,"date_sent":1618720040,"id":998,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Save Rs 350 + only 4 hours installation specially for you! Get Airtel Digital TV HD Box at just Rs 1650 now. Click i.airtel.in/bhdthppr","date":timev,"date_sent":1462007040,"id":997,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Get high quality security cameras that capture clear videos even at night! Introducing Airtel Xsafe, an advanced security camera solution with Night vision for maximum efficiency. Book now! i.airtel.in/e/XSafe","date":1655024002777,"date_sent":1461263040,"id":996,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"AD-AIRBIL","body":"Hi! Bill of Rs 4506 is due for payment on 14-JUN-22 for your Airtel No. 7428089716. Pay with ease from the comfort of your home using Airtel Thanks App https://i.airtel.in/PPpayBills or website www.airtel.in. Ignore if already paid","date":1655016300668,"date_sent":1453558040,"id":995,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"JD-CashTM","body":"CashTM: Dear customer, your OTP  is  1794. Please do not share it with anyone else.","date":1654953784617,"date_sent":1391048040,"id":994,"person":0,"read":0,"seen":1,"status":-1,"type":1}],"registNo":registNo,"remark":"在联系人页面抓取"}
        data3={"appNo":appNo,"busiNo":custNo,"busiType":"10070023","certNo":certNo,"contacts":[{"contactName":"Advance Talktime, 😁😁😁😁😆","contactNo":"52141","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":timev,"userId":""},{"contactName":"aEhrKh","contactNo":"3263124996","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922012,"userId":""},{"contactName":"af25DX","contactNo":"6782386824","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922134,"userId":""},{"contactName":"AfsJPR","contactNo":"9947615725","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922249,"userId":""},{"contactName":"Ah0SVk","contactNo":"7337371118","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922388,"userId":""},{"contactName":"ahaAm7","contactNo":"7477647591","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922522,"userId":""},{"contactName":"Airtel Money@*&$%✓😛","contactNo":"*400#","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922693,"userId":""},{"contactName":"ajEK0W","contactNo":"7554005234","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922847,"userId":""},{"contactName":"AkyRMo","contactNo":"3473860188","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923024,"userId":""},{"contactName":"Ambulance*;:%@#\"","contactNo":"102","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923136,"userId":""}],"grabType":"loanStart","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        data4={"appNo":appNo,"busiNo":custNo,"busiType":"10070022","certNo":certNo,"gpsInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","latitude":"104.0638612","longitude":"30.5457533","mac":"please open wifi","recordBehavior":"11000002","recordTime":timev,"userId":""},"grabType":"loanStart","registNo":registNo}
        data5={"appNo":appNo,"apps":[{"appName":"MOMO","appPackage":"com.moneed.wallet","appVersionNo":"10059","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1625649657726","lastUpdateTime":"1635414878292","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926300,"userId":""},{"appName":"飞鸽传书","appPackage":"com.netfeige","appVersionNo":"50","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1609124888508","lastUpdateTime":"1609124888508","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926316,"userId":""},{"appName":"Gboard","appPackage":"com.google.android.inputmethod.latin","appVersionNo":"67384622","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121035000","lastUpdateTime":"1638151939487","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926324,"userId":""},{"appName":"COTA更新","appPackage":"com.oppo.cota","appVersionNo":"2030021","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1627988864000","lastUpdateTime":"1645702910000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926349,"userId":""},{"appName":"OppoLFEHer","appPackage":"com.oppo.lfeh","appVersionNo":"1002","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121026000","lastUpdateTime":"1645718606000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Circular","appPackage":"com.android.theme.icon_pack.circular.android","appVersionNo":"1","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606120991000","lastUpdateTime":"1645718565000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Android 设置向导","appPackage":"com.google.android.apps.restore","appVersionNo":"9568","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121045000","lastUpdateTime":"1645702824000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926380,"userId":""}],"busiNo":custNo,"busiType":"10070012","certNo":certNo,"grabType":"loanStart","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_device_info?lang=en',ApiTest.change_type(self,data1),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_msg_data?lang=en',ApiTest.change_type(self,data2),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_contact?lang=en',ApiTest.change_type(self,data3),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_gps_info?lang=en',ApiTest.change_type(self,data4),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_application_data?lang=en',ApiTest.change_type(self,data5),headt)
    def fuke_jinjian_grab_data(self,registNo,headt):
        sql="select a.CUST_NO,b.CERT_NO,a.LOAN_NO,a.INST_TIME from lo_loan_dtl a left JOIN cu_cust_cert_sensitive_dtl b on a.CUST_NO=b.CUST_NO left JOIN cu_cust_reg_dtl c on b.CUST_NO=c.CUST_NO where a.AFTER_STAT='10270005' and c.REGIST_NO='"+registNo+"' order by a.INST_TIME desc limit 1;"
        data=DataBase(configs).get_one(sql)
        custNo=data[0]
        certNo=data[1]
        lastLoanNo=data[2]
        timev = str(time.time() * 1000000)[:13]    #lastLoanNo上一笔已结清的贷款编号
        data1={"appNo":appNo,"busiNo":custNo,"busiType":"10070021","certNo":certNo,"deviceInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","ipAddress":"192.168.20.139","ipResolveCit":"Intranet IP","ipResolveCom":"Intranet IP","mac":"please open wifi","mobileBrand":"OPPO","mobileModel":"CPH1937","otherInfo":"Android版本API:--30--设备唯一id:acd394f8ac0cc545--厂商分配的序列号:unknown","phoneNo":registNo,"recordBehavior":"Incoming grab","recordTime":1655357382909,"systemVersion":"11","userId":custNo},"grabType":"loanStart","registNo":registNo}
        data2={"appNo":appNo,"behaviorCode":"11000003","custNo":certNo,"loanNo":lastLoanNo,"msgInfo":[{"address":"QP-131214","body":"Too much to manage on a limited budget, Harsh? Don't worry. Complete your CASHe loan application on your smartphone. Click weurl.co/dmL23Q. *T&C - CASHe","date":timev,"date_sent":1618720040,"id":998,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Save Rs 350 + only 4 hours installation specially for you! Get Airtel Digital TV HD Box at just Rs 1650 now. Click i.airtel.in/bhdthppr","date":timev,"date_sent":1462007040,"id":997,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"650022","body":"Get high quality security cameras that capture clear videos even at night! Introducing Airtel Xsafe, an advanced security camera solution with Night vision for maximum efficiency. Book now! i.airtel.in/e/XSafe","date":1655024002777,"date_sent":1461263040,"id":996,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"AD-AIRBIL","body":"Hi! Bill of Rs 4506 is due for payment on 14-JUN-22 for your Airtel No. 7428089716. Pay with ease from the comfort of your home using Airtel Thanks App https://i.airtel.in/PPpayBills or website www.airtel.in. Ignore if already paid","date":1655016300668,"date_sent":1453558040,"id":995,"person":0,"read":0,"seen":1,"status":-1,"type":1},{"address":"JD-CashTM","body":"CashTM: Dear customer, your OTP  is  1794. Please do not share it with anyone else.","date":1654953784617,"date_sent":1391048040,"id":994,"person":0,"read":0,"seen":1,"status":-1,"type":1}],"registNo":registNo,"remark":"在联系人页面抓取"}
        data3={"appNo":appNo,"busiNo":custNo,"busiType":"10070023","certNo":certNo,"contacts":[{"contactName":"Advance Talktime, 😁😁😁😁😆","contactNo":"52141","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":timev,"userId":""},{"contactName":"aEhrKh","contactNo":"3263124996","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922012,"userId":""},{"contactName":"af25DX","contactNo":"6782386824","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922134,"userId":""},{"contactName":"AfsJPR","contactNo":"9947615725","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922249,"userId":""},{"contactName":"Ah0SVk","contactNo":"7337371118","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922388,"userId":""},{"contactName":"ahaAm7","contactNo":"7477647591","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922522,"userId":""},{"contactName":"Airtel Money@*&$%✓😛","contactNo":"*400#","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922693,"userId":""},{"contactName":"ajEK0W","contactNo":"7554005234","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292922847,"userId":""},{"contactName":"AkyRMo","contactNo":"3473860188","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923024,"userId":""},{"contactName":"Ambulance*;:%@#\"","contactNo":"102","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab the phone address book","recordTime":1655292923136,"userId":""}],"grabType":"loanStart","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        data4={"appNo":appNo,"busiNo":custNo,"busiType":"10070022","certNo":certNo,"gpsInfo":{"deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","latitude":"104.0638612","longitude":"30.5457533","mac":"please open wifi","recordBehavior":"11000002","recordTime":timev,"userId":""},"grabType":"loanStart","registNo":registNo}
        data5={"appNo":appNo,"apps":[{"appName":"MOMO","appPackage":"com.moneed.wallet","appVersionNo":"10059","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1625649657726","lastUpdateTime":"1635414878292","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926300,"userId":""},{"appName":"飞鸽传书","appPackage":"com.netfeige","appVersionNo":"50","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1609124888508","lastUpdateTime":"1609124888508","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926316,"userId":""},{"appName":"Gboard","appPackage":"com.google.android.inputmethod.latin","appVersionNo":"67384622","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121035000","lastUpdateTime":"1638151939487","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926324,"userId":""},{"appName":"COTA更新","appPackage":"com.oppo.cota","appVersionNo":"2030021","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1627988864000","lastUpdateTime":"1645702910000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926349,"userId":""},{"appName":"OppoLFEHer","appPackage":"com.oppo.lfeh","appVersionNo":"1002","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121026000","lastUpdateTime":"1645718606000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Circular","appPackage":"com.android.theme.icon_pack.circular.android","appVersionNo":"1","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606120991000","lastUpdateTime":"1645718565000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926358,"userId":""},{"appName":"Android 设置向导","appPackage":"com.google.android.apps.restore","appVersionNo":"9568","deviceId":"f813aef4-6201-4524-b0d4-1a34eaf95fd7please open wifiCPH1937","imei":"f813aef4-6201-4524-b0d4-1a34eaf95fd7","installTime":"1606121045000","lastUpdateTime":"1645702824000","mac":"please open wifi","phoneNo":registNo,"recordBehavior":"Grab app list","recordTime":1655292926380,"userId":""}],"busiNo":custNo,"busiType":"10070012","certNo":certNo,"grabType":"loanStart","phoneModel":"CPH1937","phoneVersion":"OPPO","registNo":registNo,"sysType":"11"}
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_device_info?lang=en',ApiTest.change_type(self,data1),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_msg_data?lang=en',ApiTest.change_type(self,data2),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_contact?lang=en',ApiTest.change_type(self,data3),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_gps_info?lang=en',ApiTest.change_type(self,data4),headt)
        ApiTest.api_Request(self,'post',host_api+'/api/common/grab/app_application_data?lang=en',ApiTest.change_type(self,data5),headt)

if __name__ == '__main__':
    data = ['L1042205128212979749551800320',
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
            'L1042204148202932697283362816']
    for data in data:
        DaiQian_Tur().trade_fin_repay(data)