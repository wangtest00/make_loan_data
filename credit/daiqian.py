import random
import requests

from database.credit_database import *
from make_loan_data.credit.heads import *
from make_loan_data.credit.mex_mgt import *
from make_loan_data.public.check_api import *


#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")



#短信验证码，默认手机号后4位单个+5后取个位数，在逆序排列。注意非中国手机号规则.现在实际规则改为手机号后6位。。。没区别
def compute_code(m):
    m=m[-4:]
    x1=str(int(m[0])+5)
    x2=str(int(m[1])+5)
    x3=str(int(m[2])+5)
    x4=str(int(m[3])+5)
    x=x4[-1:]+x3[-1:]+x2[-1:]+x1[-1:]
    return x
#登录前获取用户状态接口
def check_userState(registNo):
    data={"registNo":registNo}
    r=requests.post(host_api+"/api/cust/check/user/state",data=json.dumps(data),headers=head_api,verify=False)
    check_api(r)
    return r.json()
#注册登录接口。第一次验证码注册登录，返回token
def login_code(phoneNo):
    code=compute_code(phoneNo)
    t=check_userState(phoneNo)  #获取用户的状态，即是否开启密码登录
    data={"code":code,"hasPwd":t['data']['hasPwd'],"phoneNo":phoneNo}
    r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
    try:
        c=check_api(r)
        if c!=0:
            t=r.json()
            token=t['data']['token']
            return token
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
#（通过密码）登录接口，返回token
def login_pwd(phoneNo):
    t = check_userState(phoneNo)  # 获取用户的状态，即是否开启密码登录
    data={"phoneNo":phoneNo,"password":"123456","hasPwd":t['data']['hasPwd']}
    r=requests.post(host_api+"/api/cust/pwd/login",data=json.dumps(data),headers=head_api,verify=False)
    try:
        c=check_api(r)
        if c!=0:
            t=r.json()
            token=t['data']['token']
            return token
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
#更新登录密码接口，包含了用验证码方式注册登录的步骤
def update_pwd(phoneNo):
    token=login_code(phoneNo)
    headt=head_token(token)
    data={"phoneNo":phoneNo,"newPwd":"123456"}
    r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data),headers=headt,verify=False)
    check_api(r)
#获得第三方授权接口
def third_track_detail(registNo,headt2):
    timev=str(time.time()*1000000)[:13]
    code=compute_code(registNo)
    data1={"phoneNo":registNo,"enventList":[{"eventId":"login_otp_no_pw","label":"enter_the_page","key":"in","value":timev,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20",
        "networkType":"1","recordTime":timev,"timeOnline":"","remark":""},{"eventId":"login_otp_no_pw","label":"fill_in_otp","key":"standing_time","value":"4298","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1","recordTime":timev,"timeOnline":"","remark":""},
        {"eventId":"login_otp_no_pw","label":"fill_in_otp","key":"content","value":code,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1","recordTime":timev,"timeOnline":"","remark":""}],"androidId":"274b98eb5c8aed06","custNo":"","loanNo":""}
    data2={"phoneNo":registNo,"enventList":[{"eventId":"password_set","label":"enter_the_page","key":"in","value":timev,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1",
                                            "recordTime":timev,"timeOnline":"","remark":""}],"androidId":"274b98eb5c8aed06","custNo":"","loanNo":""}
    print(host_action+"/api/third/track/detail")
    r1=requests.post(host_action+"/api/third/track/detail",data=json.dumps(data1),headers=headt2)
    check_api(r1)
    r2=requests.post(host_action+"/api/third/track/detail",data=json.dumps(data2),headers=headt2,verify=False)
    check_api(r2)
    data3={"phoneNo":registNo,"enventList":[{"eventId":"password_set","label":"set_password","key":"standing_time","value":"3277","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20",
    "networkType":"1","recordTime":timev,"timeOnline":"","remark":""},{"eventId":"password_set","label":"set_password","key":"content","value":"123456","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1","recordTime":timev,"timeOnline":"","remark":""},
    {"eventId":"confirm_password","label":"enter_the_page","key":"in","value":timev,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1",
    "recordTime":timev,"timeOnline":"","remark":""},{"eventId":"confirm_password","label":"confirm_password","key":"standing_time","value":"2453","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20",
    "networkType":"1","recordTime":timev,"timeOnline":"","remark":""},{"eventId":"confirm_password","label":"confirm_password","key":"content","value":"123456","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20",
    "networkType":"1","recordTime":timev,"timeOnline":"","remark":""}],"androidId":"274b98eb5c8aed06","custNo":"","loanNo":""}
    r3=requests.post(host_action+"/api/third/track/detail",data=json.dumps(data3),headers=headt2,verify=False)
    check_api(r3)
#第一个页面，注册认证接口，获得custNo
def auth_cert(registNo,headt):
    st=''
    for j in range(4):  #生成4个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    data={"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005",
          "fatherLastName":"AUTO","gender":"10030001","lockKey":"",
          "motherLastName":"TEST","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
    r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data),headers=headt,verify=False)
    t=check_api(r)
    if t!=0:
        return t['data']['custNo']
    else:
        pass
#第二个页面。暂时有问题，不可用
def kyc_auth(registNo,custNo,headt):
    files={'kycImg':('1.jpg',open(r'D:\pic\1.jpg', 'rb'),'image/jpeg'),'custNo':(None,custNo),'kycType':(None,'10070001') }
    r=requests.post(host_api+"/api/cust/auth/kyc",files=files,headers=headt)
    check_api(r)
#第三个页面，工作信息认证接口
def auth_work(custNo,headt):
    data1={"certType":"WORK","custNo":custNo}
    r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=headt,verify=False)
    check_api(r1)
    data2={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
    r2=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=headt,verify=False)
    check_api(r2)

def auth_review_contact(custNo,headt):
    data3={"certType":"CONTACT","custNo":custNo}
    r3=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data3),headers=headt,verify=False)
    check_api(r3)
#抓取数据接口
def auth_app_grab_data(phoneNo,custNo,headt):
    #设备信息
    data4={"appNo":appNo,"phoneNo":phoneNo,"dataType":"11090003","pageGet":"Contact","recordTime":"1621332187810","grabData":{"ipAddress":"2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCit":"2409:8162:a46:5405:1:0:107f:acec%20",
    "ipResolveCom":"2409:8162:a46:5405:1:0:107f:acec%20","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"抓取设备数据","recordTime":"1621332187810","userId":custNo,"mobileBrand":"HUAWEI","mobileModel":"LIO-AL00","systemVersion":"10","otherInfo":"274b98eb5c8aed06"},"custNo":custNo}
    #联系人
    data5={"appNo":appNo,"phoneNo":phoneNo,"dataType":"11090002","pageGet":"Contact","recordTime":"1621332187811","grabData":{"data":
    [{"contactName":"test","contactNo":"888 845 5666","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc",
      "mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取","recordTime":"1621332187811","userId":custNo},{"contactName":"test2","contactNo":"888 335 5777",
    "deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"联系人列表抓取",
    "recordTime":"1621332187811","userId":custNo}]},"custNo":custNo}
    #短信内容
    data6={"appNo":appNo,"phoneNo":phoneNo,"dataType":"11090005","pageGet":"Contact","recordTime":"1621332187836","grabData":{"data":[{"body":"【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。","address":"95599","date":"2021-05-18 17:02:48.863","dateSent":"2021-05-18 17:02:46.000","sender":"95599","kind":"SmsMessageKind.Received"}]},"custNo":custNo}
    #位置信息
    data7={"appNo":appNo,"phoneNo":phoneNo,"dataType":"11090004","pageGet":"Contact","recordTime":"1621332187838","grabData":{"latitude":"30.550366","longitude":"104.062236","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"11000003","recordTime":"1621332187838","userId":custNo},"custNo":custNo}
    #已安装应用
    data8={"appNo":appNo,"phoneNo":phoneNo,"dataType":"11090001","pageGet":"Contact","recordTime":"1621332187731","grabData":{"data":[{"appName":"安全教育平台","appPackage":"com.jzzs.ParentsHelper","appVersionNo":"1.7.0","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","installTime":1599480832637,"lastUpdateTime":1618934047038,"mac":"A2:B4:74:63:FB:40","phoneNo":phoneNo,"recordBehavior":"App列表抓取","recordTime":"1621332187731","userId":custNo}]},"custNo":custNo}
    data0=[data4,data5,data6,data7,data8]
    for data0 in data0:
        r0=requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=headt,verify=False)  #抓取用户手机设备信息，短信，通讯录，已安装app，位置信息
        check_api(r0)
        time.sleep(1)
# 第四个页面，其他联系人信息认证接口
def auth_contact(custNo,headt):
    #data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
    data9={"custNo":custNo,"contacts":[{"custNo":custNo,"name":"test1","phone":"123333","relationship":"10110004","relationshipName":"Hermanos"},{"custNo":custNo,"name":"test2","phone":"543212601","relationship":"10110001","relationshipName":"Padres"}]}
    r9=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=headt,verify=False)#最后一步，填写2个联系人的联系方式
    check_api(r9)

#查看认证信息接口，查看银行卡绑卡现状和历史绑卡信息
def auth_review_bank(custNo,headt):
    data = {"certType": "BANK", "custNo": custNo}
    r = requests.post(host_api + '/api/cust/auth/review', data=json.dumps(data), headers=headt,verify=False)
    check_api(r)
#更新KYC认证状态及照片路径
def update_kyc_auth(phoneNo,custNo):
    t=str(time.time()*1000000)[:15]
    tnum1=str(random.randrange(10000,99999))
    tnum2=str(random.randrange(10000,99999))
    tnum3=str(random.randrange(10000,99999))
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    riqi=str(datetime.datetime.now().strftime('%Y%m%d'))
    sql="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
    DataBase(which_db).executeUpdateSql(sql)
    sql2="INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+phoneNo+"', '"+custNo+"','"+appNo+"', '10070001', '100700011634111496160.jpg', '100700011634111496160.jpg', NULL, '.jpg', '132755', '208/20211013/3218375163/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+phoneNo+"', '"+custNo+"','"+appNo+"', '10070002', '100700021634111507015.jpg', '100700021634111507015.jpg', NULL, '.jpg', '142126',  '208/20211013/3218375163/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO `mex_credit`.`cu_cust_file_dtl`(`ID`, `PHONE_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+phoneNo+"', '"+custNo+"','"+appNo+"', '10070004', '100700041634111518981.jpg', '100700041634111518981.jpg', NULL, '.jpg', '107642',  '208/20211013/3218375163/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(which_db).executeUpdateSql(sql2)
    DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).executeUpdateSql(sql4)

#绑定银行卡接口，需要把银行卡号改成明显错的，环境怕放出真实的钱
def auth_bank(custNo,headt):
    #bank_acct_no=str(random.randint(100000,999999))
    data={"bankCode":"10020008","bankCodeName":"BBVA BANCOMER","clabe":"012121212121212128","custNo":custNo}
    r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt,verify=False)
    check_api(r)                                         #改为6位随机数
   # sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
   # DataBase(which_db).executeUpdateSql(sql)

#风控授信调度接口：api调风控，获得风控回调结果
def risk_credit(headt):
    r = requests.post(host_api+'/api/task/risk/credit',headers=headt,verify=False)
    check_api(r)
    print("api调风控接口，获得风控回调结果")

def cx_risk_and_approve(custNo):
    sql="select RISK_LEVEL from cu_credit_risk_order_dtl where BUSINESS_NO='"+custNo+"';"
    risk_level=DataBase('mex_credit').get_one(sql)
    print(risk_level)
    if risk_level is not None:
        if risk_level[0]=='AA':
            print("风控自动通过",custNo)
        else:
            print("走人审，需要跑分案存储过程",custNo)
            DataBase('mex_credit').call_proc_apr_appr_allocation_control()
            approve(custNo)
    else:
        print("风控未回调给api授信结果, 请检查风控",custNo)
    return risk_level

#模拟银行回调-放款,可能会调失败
def web_hook_payout_stp():
    delay_payout_handler()
    #sql="select tran_no,tran_order_no from pay_tran_dtl where tran_no=(select ORDER_NO from lo_loan_payout_dtl where LOAN_NO=(select loan_no from lo_loan_dtl  where CUST_NO='"+cust_no+"')); "
    #print(sql)
    sql="select TRAN_NO,TRAN_ORDER_NO from pay_tran_dtl t where  t.TRAN_TYPE='10320003'  and IN_ACCT_NO='012121212121212128' and  ACT_TRAN_AMT is null  order by INST_TIME desc limit 1;"
    list=DataBase(which_db).get_one(sql)
    print(list)
    data={
    "causaDevolucion": {
        "code": 16,
        "msg": "Tipo de operación errónea"
    },
    "empresa": "ASSERTIVE",
    "estado": {
        "code": "0000",   #非0000，则模拟到放款失败
        "msg": "canll"
    },
    "folioOrigen": list[0],
    "id": int(list[1])
}
    r=requests.post(host_pay+'/api/web_hook/payout/stp',data=json.dumps(data),headers=head_pay,verify=False)
    print(r.json())
#唤醒延迟放款
def delay_payout_handler():
    for i in range(1):
        r=requests.post(host_api+"/api/credit/payment/anon/delay_payout_handler",headers=head_api,verify=False)
        check_api(r)
        time.sleep(3)

def payment_detail(headt):
    r=requests.post(host_api+"/api/credit/payment/detail",headers=headt,verify=False)
    check_api(r)
def payment(headt):
    data={"withdrawAmt":"500.0"}
    r=requests.post(host_api+"/api/credit/payment",data=json.dumps(data),headers=headt,verify=False)
    check_api(r)

#检查放款成功
def check_stat_fk(cust_no):
    sql="select BEFORE_STAT,AFTER_STAT from lo_loan_dtl t where CUST_NO='"+cust_no+"' order by INST_TIME desc limit 1;"
    res=DataBase(which_db).get_one(sql)
    if res[0]=='10260005' and res[1]=='10270002':
        print("【贷前提现成功，贷后正常】",cust_no)
    else:
        print("【贷前贷后状态未更新】",cust_no)
#检查还款结清
def check_stat_jq(cust_no):
    sql="select BEFORE_STAT,AFTER_STAT from lo_loan_dtl t where CUST_NO='"+cust_no+"' order by INST_TIME desc limit 1;"
    res=DataBase(which_db).get_one(sql)
    if res[0]=='10260005' and res[1]=='10270005':
        print("【lo_loan_dtl表状态已更新为-已结清】",cust_no)
    else:
        print("【lo_loan_dtl表状态未更新】",cust_no)
    sql2="select BILL_STATUS from cu_cust_bill_dtl  where cust_no='"+cust_no+"';"
    res2=DataBase(which_db).get_one(sql2)
    res2=res2[0]
    if res2=='20060001':
        print("【cu_cust_bill_dtl表状态已更新-已结清】",cust_no)
    else:
        print("【cu_cust_bill_dtl表未更新】",cust_no)

def withdraw(headt):
    payment_detail(headt)
    payment(headt)

if __name__ == '__main__':
    #chaxun_risk_level('C2082110148136936439893131264')
    #web_hook_payout_stp()
    delay_payout_handler()