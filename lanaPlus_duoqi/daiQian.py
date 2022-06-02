from lanaPlus_duoqi.heads_mex import *
from lanaPlus_duoqi.mgt_Duoqi import *
from data.var_mex_lp_duoqi import *
import random,datetime,string
from common.commUrl_mex import *
from common.api_Request import *

class ApiTest(Api_Request):
    def __init__(self):
        self.apiTestName=Api_Request()

class DaiQian_Duoqi(ApiTest):
    #第一次验证码注册登录，返回token
    def login_code(self,registNo,code):
        data1 = {"registNo": registNo, "code": code, "gaid": shenpiren[appNo][5], "channelNo": ""}
        t=ApiTest.api_Request(self,'post',host_api+loginUrl,ApiTest.change_type(self,data1),head_api)
        if t!=0:
            token=t['data']['token']
            return token
        else:
            return 0
    #通过密码登录，返回token
    def login_pwd(self,registNo):
        data2 = {"registNo": registNo, "password": "123456", "gaid": shenpiren[appNo][5], "channelNo": ""}
        t=ApiTest.api_Request(self,'post',host_api+loginPwdUrl,ApiTest.change_type(self,data2),head_api)
        if t!=0:
            token=t['data']['token']
            return token
        else:
            return 0
    #更新登录密码，包含了用验证码方式注册登录的步骤
    def update_pwd(self,registNo,headt):
        data3 = {"registNo": registNo, "newPwd": "123456"}
        r=ApiTest.api_Request(self,'post',host_api+updatePwdUrl,ApiTest.change_type(self,data3),headt)
    #获得第三方授权后，埋点
    def third_track_detail(self,registNo,code,headt):
        timev = str(time.time() * 1000000)[:13]
        data4 = {"phoneNo": registNo, "enventList": [
            {"eventId": "login_otp_no_pw", "label": "enter_the_page", "key": "in", "value": timev,
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "login_otp_no_pw", "label": "fill_in_otp", "key": "standing_time", "value": "4298",
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "login_otp_no_pw", "label": "fill_in_otp", "key": "content", "value": code,
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""}], "androidId": "274b98eb5c8aed06", "custNo": "", "loanNo": ""}
        data5 = {"phoneNo": registNo, "enventList": [
            {"eventId": "password_set", "label": "enter_the_page", "key": "in", "value": timev,
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""}], "androidId": "274b98eb5c8aed06", "custNo": "", "loanNo": ""}
        data6 = {"phoneNo": registNo, "enventList": [
            {"eventId": "password_set", "label": "set_password", "key": "standing_time", "value": "3277",
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "password_set", "label": "set_password", "key": "content", "value": "123456",
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "confirm_password", "label": "enter_the_page", "key": "in", "value": timev,
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "confirm_password", "label": "confirm_password", "key": "standing_time", "value": "2453",
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""},
            {"eventId": "confirm_password", "label": "confirm_password", "key": "content", "value": "123456",
             "innerNetworkIp": "2409:8162:a46:5405:1:0:107f:acec%20", "networkType": "1", "recordTime": timev,
             "timeOnline": "", "remark": ""}], "androidId": "274b98eb5c8aed06", "custNo": "", "loanNo": ""}
        r1=ApiTest.api_Request(self,'post',host_action+trackDetailUrl,ApiTest.change_type(self,data4),headt)
        r2=ApiTest.api_Request(self,'post',host_action+trackDetailUrl,ApiTest.change_type(self,data5),headt)
        r3=ApiTest.api_Request(self,'post',host_action+trackDetailUrl,ApiTest.change_type(self,data6),headt)
    #1.第一个页面，注册认证，获得custNo
    def auth_cert(self,registNo,headt):
        st = ''
        for j in range(4):  # 生成4个随机英文大写字母
            st += random.choice(string.ascii_uppercase)
        data7 = {"birthdate": "1999-3-19", "civilStatus": "10050001", "curp": st + "990319MM" + st + "V8",
                 "delegationOrMunicipality": "zxcvbbbccxxx", "education": "10190005",
                 "fatherLastName": "SHUANG", "gender": "10030001", "motherLastName": "TEST", "name": "AUTO",
                 "outdoorNumber": "qweetyyu", "phoneNo": registNo, "postalCode": "55555", "state": "11130001",
                 "street": "444444", "suburb": "asdfhhj", "email": ""}
        t=ApiTest.api_Request(self,'post',host_api+certAuthUrl,ApiTest.change_type(self,data7),headt)
        if t!=0:
            return t['data']['custNo']
        else:
            pass
    #第二个页面。暂时有问题，不可用
    def kyc_auth(self,registNo,custNo,headt):
        files={'kycImg':('1.jpg',open(r'D:\pic\1.jpg', 'rb'),'image/jpeg'),'custNo':(None,custNo),'kycType':(None,'10070001') }
        r=requests.post(host_api+"/api/cust/auth/kyc",files=files,headers=headt)

    def auth_work(self,custNo,headt):
        data8 = {"certType": "WORK", "custNo": custNo}
        data9 = {"companyAddress": "", "companyName": "", "companyPhone": "", "custNo": custNo, "income": "10870004","industry": "", "jobType": "10130006"}  # 工作收入来源
        r1=ApiTest.api_Request(self,'post',host_api+authReviewUrl,ApiTest.change_type(self,data8),headt)
        r2=ApiTest.api_Request(self,'post',host_api+workAuthUrl,ApiTest.change_type(self,data9),headt)

    def auth_review_contact(self,custNo,headt):
        data10 = {"certType": "CONTACT", "custNo": custNo}
        r=ApiTest.api_Request(self,'post',host_api+authReviewUrl,ApiTest.change_type(self,data10),headt)

    # 抓取用户手机短信，通讯录，已安装app等信息
    def auth_app_grab_data(self,registNo,custNo,headt):
        imei = 'a2eff92b-86cb-6666-a66c-84ae322f3adc'
        # 设备信息
        data11 = {"appNo": appNo, "phoneNo": registNo, "dataType": "11090003", "pageGet": "10000001","recordTime": "1621332187810","grabData": {"ipAddress": "192.188.99.99", "ipResolveCit": "2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCom": "2409:8162:a46:5405:1:0:107f:acec%20","deviceId": "a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei": imei,"mac": "A2:B4:74:63:FB:40", "phoneNo": registNo, "recordBehavior": "抓取设备数据","recordTime": "1621332187810", "userId": custNo, "mobileBrand": "HUAWEI","mobileModel": "LIO-AL00", "systemVersion": "10", "otherInfo": "274b98eb5c8aed06"},"custNo": custNo}
        # 联系人
        data12 = {"appNo": appNo, "phoneNo": registNo, "dataType": "11090002", "pageGet": "10000001","recordTime": "1621332187811", "grabData": {"data": [{"contactName": "test", "contactNo": "888 845 5666","deviceId": "a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00", "imei": imei,"mac": "A2:B4:74:63:FB:40", "phoneNo": registNo, "recordBehavior": "联系人列表抓取","recordTime": "1621332187811", "userId": custNo}, {"contactName": "test2", "contactNo": "888 335 5777","deviceId": "a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei": imei, "mac": "A2:B4:74:63:FB:40","phoneNo": registNo, "recordBehavior": "联系人列表抓取","recordTime": "1621332187811", "userId": custNo}]},"custNo": custNo}
        # 短信内容
        data13 = {"appNo": appNo, "phoneNo": registNo, "dataType": "11090005", "pageGet": "10000001","recordTime": "1621332187836", "grabData": {"data": [{"body": "【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。", "address": "95599","date": "2021-05-18 17:02:48.863", "dateSent": "2021-05-18 17:02:46.000", "sender": "95599","kind": "SmsMessageKind.Received"}]}, "custNo": custNo}
        # 设备信息
        data14 = {"appNo": appNo, "phoneNo": registNo, "dataType": "11090004", "pageGet": "10000001","recordTime": "1621332187838", "grabData": {"latitude": "30.550366", "longitude": "104.062236","deviceId": "a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei": imei, "mac": "A2:B4:74:63:FB:40","phoneNo": registNo, "recordBehavior": "11000003","recordTime": "1621332187838", "userId": custNo},"custNo": custNo}
        # 已安装应用
        data15 = {"appNo": appNo, "phoneNo": registNo, "dataType": "11090001", "pageGet": "10000001","recordTime": "1621332187731", "grabData": {"data": [{"appName": "安全教育平台", "appPackage": "com.jzzs.ParentsHelper", "appVersionNo": "1.7.0","deviceId": "a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00", "imei": imei,"installTime": 1599480832637, "lastUpdateTime": 1618934047038, "mac": "A2:B4:74:63:FB:40","phoneNo": registNo, "recordBehavior": "App列表抓取", "recordTime": "1621332187731","userId": custNo}]}, "custNo": custNo}
        data=[data11,data12,data13,data14,data15]
        for data in data:
            r=ApiTest.api_Request(self,'post',host_api+grabDataUrl,ApiTest.change_type(self,data),headt)
    # 最后一步，填写2个联系人的联系方式
    def auth_contact(self,custNo,headt):
        # 第4个页面，其他联系人
        data16 = {"contacts": [{"name": "test", "phone": "8888455666", "relationship": "10110004"},
                               {"name": "test2", "phone": "8883355777", "relationship": "10110003"}], "custNo": custNo}
        r=ApiTest.api_Request(self,'post',host_api+contactAuthUrl,ApiTest.change_type(self,data16),headt)
    #4个认证都通过后调申请贷款接口
    def apply_loan(self,custNo,headt):
        data17 = {"custNo": custNo}
        r=ApiTest.api_Request(self,'post',host_api+withdrawUrl,ApiTest.change_type(self,data17),headt)
        return r['data']['loanNo']
    #更新kyc认证状态及其值
    def update_kyc_auth(self,registNo,custNo):
        t=str(time.time()*1000000)[:15]
        tnum1=str(random.randrange(10000,99999))
        tnum2=str(random.randrange(10000,99999))
        tnum3=str(random.randrange(10000,99999))
        inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql1="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
        DataBase(which_db).executeUpdateSql(sql1)
        sql2="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070001', '100700011632400318577.jpg', '100700011632400318577.jpg', NULL, '.jpg', '677710', '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        sql3="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070002', '100700021632400319381.jpg', '100700021632400319381.jpg', NULL, '.jpg', '704805',  '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        sql4="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070004', '100700041632400322001.jpg', '100700041632400322001.jpg', NULL, '.jpg', '206389',  '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
        DataBase(which_db).executeUpdateSql(sql2)
        DataBase(which_db).executeUpdateSql(sql3)
        DataBase(which_db).executeUpdateSql(sql4)
    #绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱
    def bank_auth(self,custNo,headt):
        bank_acct_no=str(random.randint(100000,999999))
        data18 = {"bankCode": "10020037", "clabe": "138455214411441105", "custNo": custNo}
        r=ApiTest.api_Request(self,'post',host_api+bankAuthUrl,ApiTest.change_type(self,data18),headt)
        time.sleep(1)                                         #改为6位随机数
        sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"#修改成随机卡号，避免触发绑卡被拒:同一张银行卡不能被超过2个人绑定并放款成功
        DataBase(which_db).executeUpdateSql(sql)
    #提现接口-app点击提现按钮
    def withdraw(self,registNo,custNo,loanNo,headt):
        t=ApiTest.api_Request(self,'get',host_api+'/api/loan/latest/'+registNo,'',headt)#获取最近一笔贷款贷款金额，注意请求头content-length的值。The request body did not contain the specified number of bytes. Got 0, expected 63
        print('产品配置长度=',len(t['data']['trailPaymentDetail']))
        if t['errorCode']==0:
            loanAmt=t['data']['trailPaymentDetail'][0]['loanAmt']
            instNum=t['data']['trailPaymentDetail'][0]['instNum']
            data19 = {"custNo": custNo, "instNum": instNum, "loanAmt": loanAmt, "loanNo": loanNo, "prodNo": prodNo}
            r2=ApiTest.api_Request(self,'post',host_api+confirmWithdrawUrl,ApiTest.change_type(self,data19),headt)
            return 1
        else:
            print("待提现页面，未获取到最近一笔贷款的数据,不去做改数操作")
            return 0
    #当前时间的前一天=跑批业务日期，才能正常申请借款
    def update_batch_log(self):
        sql='select now();'
        date_time=DataBase(which_db).get_one(sql)
        day=str(date_time[0]+datetime.timedelta(days=-1))
        yudate=day[:4]+day[5:7]+day[8:10]
        sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
        BUSI_DATE=DataBase(which_db).get_one(sql2)
        if yudate==BUSI_DATE[0]:
            print("当前服务器日期为:",date_time[0])
            print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
        else:
            sql3="update sys_batch_log set BUSI_DATE='"+yudate+"',BATCH_STAT='10490002',IS_PROD_SEL='10000001' where BUSI_DATE='"+BUSI_DATE[0]+"';"
            DataBase(which_db).executeUpdateSql(sql3)
        DataBase(which_db).closeDB()
    #获取所有账单日
    def getRepayDateList(self,registNo,headt):
        r=requests.get(host_api+'/api/loan/latest/'+registNo,headers=headt)#获取最近一笔贷款贷款金额，注意请求头content-length的值。The request body did not contain the specified number of bytes. Got 0, expected 63
        t=r.json()
        if t['errorCode']==0:
            repayDateList=[]
            repaymentDetailList=t['data']['repaymentDetail']['repaymentDetailList']
            for i in range(len(repaymentDetailList)):
                if t['data']['repaymentDetail']['repaymentDetailList'][i]['stat']!='SETTLE_MENT':
                    repayDate=t['data']['repaymentDetail']['repaymentDetailList'][i]['repayDate']
                    repayDate=repayDate[:10]
                    timeArray = time.localtime(int(repayDate[:10]))
                    repayDate = time.strftime("%Y%m%d", timeArray)#时间戳转日期
                    repayDateList.append(repayDate)
                    print(repayDateList)
                    return repayDateList
                else:
                    pass
        else:
            return 0

    def repay(self,custNo,loanNo,repayDate,headt):                                                           #OXXO用CONEKTA
        data={"advance":"10000000","custNo":custNo,"defer":False,"loanNo":loanNo,"paymentMethod":"STP","repayDateList":[repayDate],"tranAppType":"Android"}
        m=ApiTest.api_Request(self,'post',host_api+repayUrl,ApiTest.change_type(self,data),headt)
        repayList=[]
        if m!=0:
            transAmt=m['data']['stpRepayment']['transAmt']  #获取待还金额
            print(transAmt)
            repayList.append(transAmt)
        else:
            pass
        sql="select CLABE_NO from fin_clabe_usable_dtl where CUST_NO='"+custNo+"';"
        in_acct_no=DataBase(which_db).get_one(sql)
        in_acct_no=in_acct_no[0]
        if in_acct_no==None:
            print("repay接口请求有错，未向pay_tran_dtl表写入还款账号等数据",in_acct_no)
        else:
            print("repay接口请求正确，向pay_tran_dtl表写入还款账号等数据",in_acct_no)
            repayList.append(in_acct_no)
        return repayList
    #提现接口-app点击提现按钮
    def single_withdraw(self,registNo,custNo,loan_no,headt):
        loanAmt="1100.00"
        instNum='3'
        data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loan_no,"prodNo":prodNo}
        r=ApiTest.api_Request(self,'post',host_api+withdrawUrl,ApiTest.change_type(self,data),headt)
        print(r.json())

    def cx_beforeStat_afterStat(self,loanNo):
        sql='''select BEFORE_STAT,AFTER_STAT from lo_loan_dtl where LOAN_NO="'''+loanNo+'''";'''
        stat=DataBase(which_db).get_one(sql)
        return stat
if __name__ == '__main__':
    daiQian = DaiQian_Danqi()
    custNo = 'C2012205318220170660757045248'
    daiQian.login_code(registNo, code)
    daiQian.update_pwd(registNo)
    token = daiQian.login_pwd(registNo)
    headt = head_token(token)
    #custNo = daiQian.auth_cert(registNo, headt)
    daiQian.auth_work(custNo, headt)
