import string,requests,json,datetime
from public.dataBase import *
from mexico.gaishu import *
from data.var_mex import *
from mexico.mex_mgt import *
from mexico.heads import *
from public.check_api import *
import io,sys
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
#第一次验证码注册登录，返回token
def login_code(registNo):
    code=compute_code(registNo)
    data={"registNo":registNo,"code":code,"gaid":"Exception:null"}
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
#通过密码登录，返回token
def login_pwd(registNo):
    data={"registNo":registNo,"password":"123456","gaid":"Exception:null"}
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
#更新登录密码，包含了用验证码方式注册登录的步骤
def update_pwd(registNo):
    token=login_code(registNo)
    headt=head_token(token)
    data={"registNo":registNo,"newPwd":"123456"}
    r=requests.post(host_api+"/api/cust/pwd/update",data=json.dumps(data),headers=headt,verify=False)
    check_api(r)
#获得第三方授权
def third_track_detail(registNo,headt2):
    timev=str(time.time()*1000000)[:13]
    code=compute_code(registNo)
    data1={"phoneNo":registNo,"enventList":[{"eventId":"login_otp_no_pw","label":"enter_the_page","key":"in","value":timev,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20",
        "networkType":"1","recordTime":timev,"timeOnline":"","remark":""},{"eventId":"login_otp_no_pw","label":"fill_in_otp","key":"standing_time","value":"4298","innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1","recordTime":timev,"timeOnline":"","remark":""},
        {"eventId":"login_otp_no_pw","label":"fill_in_otp","key":"content","value":code,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1","recordTime":timev,"timeOnline":"","remark":""}],"androidId":"274b98eb5c8aed06","custNo":"","loanNo":""}
    data2={"phoneNo":registNo,"enventList":[{"eventId":"password_set","label":"enter_the_page","key":"in","value":timev,"innerNetworkIp":"2409:8162:a46:5405:1:0:107f:acec%20","networkType":"1",
                                            "recordTime":timev,"timeOnline":"","remark":""}],"androidId":"274b98eb5c8aed06","custNo":"","loanNo":""}
    print(data1)
    print(host_action+"/api/third/track/detail")
    r1=requests.post(host_action+"/api/third/track/detail",data=json.dumps(data1),headers=headt2)
    print(r1.status_code)
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
#1.第一个页面，注册认证，获得custNo
def auth_cert(registNo,headt):
    st=''
    for j in range(4):  #生成4个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    data={"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005","fatherLastName":"WANG","gender":"10030001",
          "motherLastName":"LIU","name":"SHUANG","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
    r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data),headers=headt)
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

def auth_work(custNo,headt):
    data1={"certType":"WORK","custNo":custNo}
    r1=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data1),headers=headt)
    check_api(r1)
    data2={"companyAddress":"","companyName":"","companyPhone":"","custNo":custNo,"income":"10870004","industry":"","jobType":"10130006"}#工作收入来源
    r2=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data2),headers=headt)
    check_api(r2)
def auth_review_contact(custNo,headt):
    data3={"certType":"CONTACT","custNo":custNo}
    r3=requests.post(host_api+'/api/cust/auth/review',data=json.dumps(data3),headers=headt)
    check_api(r3)
def auth_app_grab_data(registNo,custNo,headt):
    #设备信息
    data4={"appNo":"201","phoneNo":registNo,"dataType":"11090003","pageGet":"10000001","recordTime":"1621332187810","grabData":{"ipAddress":"2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCit":"2409:8162:a46:5405:1:0:107f:acec%20",
    "ipResolveCom":"2409:8162:a46:5405:1:0:107f:acec%20","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"抓取设备数据","recordTime":"1621332187810","userId":custNo,"mobileBrand":"HUAWEI","mobileModel":"LIO-AL00","systemVersion":"10","otherInfo":"274b98eb5c8aed06"},"custNo":custNo}
    #联系人
    data5={"appNo":"201","phoneNo":registNo,"dataType":"11090002","pageGet":"10000001","recordTime":"1621332187811","grabData":{"data":
    [{"contactName":"test","contactNo":"888 845 5666","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc",
      "mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取","recordTime":"1621332187811","userId":custNo},{"contactName":"test2","contactNo":"888 335 5777",
    "deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取",
    "recordTime":"1621332187811","userId":custNo}]},"custNo":custNo}
    #短信内容
    data6={"appNo":"201","phoneNo":registNo,"dataType":"11090005","pageGet":"10000001","recordTime":"1621332187836","grabData":{"data":[{"body":"【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。","address":"95599","date":"2021-05-18 17:02:48.863","dateSent":"2021-05-18 17:02:46.000","sender":"95599","kind":"SmsMessageKind.Received"}]},"custNo":custNo}
    #设备信息
    data7={"appNo":"201","phoneNo":registNo,"dataType":"11090004","pageGet":"10000001","recordTime":"1621332187838","grabData":{"latitude":"30.550366","longitude":"104.062236","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"11000003","recordTime":"1621332187838","userId":custNo},"custNo":custNo}
    #已安装应用
    data8={"appNo":"201","phoneNo":registNo,"dataType":"11090001","pageGet":"10000001","recordTime":"1621332187731","grabData":{"data":[{"appName":"安全教育平台","appPackage":"com.jzzs.ParentsHelper","appVersionNo":"1.7.0","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":"a2eff92b-86cb-4614-a66c-84ae322f3adc","installTime":1599480832637,"lastUpdateTime":1618934047038,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"App列表抓取","recordTime":"1621332187731","userId":custNo}]},"custNo":custNo}
    data0=[data4,data5,data6,data7,data8]
    for data0 in data0:
        r0=requests.post(host_api+'/api/common/grab/app_grab_data',data=json.dumps(data0),headers=headt)  #抓取用户手机短信，通讯录，已安装app等信息
        check_api(r0)
        time.sleep(1)
def auth_contact(custNo,headt):
    data9={"contacts":[{"name":"test","phone":"8888455666","relationship":"10110004"},{"name":"test2","phone":"8883355777","relationship":"10110003"}],"custNo":custNo}
    r9=requests.post(host_api+'/api/cust/auth/other/contact',data=json.dumps(data9),headers=headt)#最后一步，填写2个联系人的联系方式
    check_api(r9)
#4个认证都通过后调申请贷款接口
def apply_loan(custNo,headt):
    data10={"custNo":custNo}
    r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data10),headers=headt)#申请贷款
    apply=check_api(r)
    print(apply['data']['loanNo'],apply['data']['beforeStat'])
    return apply['data']['loanNo']
#更新kyc认证状态及其值
def update_kyc_auth(registNo,custNo):
    t=str(time.time()*1000000)[:15]
    tnum1=str(random.randrange(10000,99999))
    tnum2=str(random.randrange(10000,99999))
    tnum3=str(random.randrange(10000,99999))
    inst_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql="update cu_cust_auth_dtl set KYC_AUTH='1' WHERE CUST_NO='"+custNo+"';"  #客户认证信息明细表kyc认证状态
    DataBase(which_db).executeUpdateSql(sql)
    sql2="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '201', '10070001', '100700011621408803787.jpg', '100700011621408803787.jpg', NULL, '.jpg', '307350', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '201', '10070002', '100700021621408806923.jpg', '100700021621408806923.jpg', NULL, '.jpg', '317778', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '201', '10070004', '100700041621408812009.jpg', '100700041621408812009.jpg', NULL, '.jpg', '190855', '201/20210519/9999990000/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(which_db).executeUpdateSql(sql2)
    DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).executeUpdateSql(sql4)
#绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱
def bank_auth(custNo,headt):
    timev=str(time.time()*1000000)[:15]
    bank_acct_no=str(random.randint(10000,99999))
    data={"bankCode":"10020021","clabe":timev+"123","custNo":custNo}
    r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt)
    check_api(r)
    time.sleep(1)                                         #改为4位随机数
    sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"
    DataBase(which_db).executeUpdateSql(sql)
#提现接口-app点击提现按钮
def withdraw(registNo,custNo,loan_no,headt):
    r=requests.get(host_api+'/api/loan/latest/'+registNo,headers=headt)#获取最近一笔贷款贷款金额，注意请求头content-length的值。The request body did not contain the specified number of bytes. Got 0, expected 63
    check_api(r)
    t=r.json()
    if t['errorCode']==0:
        loanAmt=t['data']['loanInfoData']['feeDetail']['loanAmount']
        data={"custNo":custNo,"instNum":"1","loanAmt":loanAmt,"loanNo":loan_no,"prodNo":prodNo}
        r2=requests.post(host_api+'/api/trade/fin/withdraw',data=json.dumps(data),headers=headt)
        check_api(r2)
        return 1
    else:
        print("待提现页面，未获取到该笔贷款的数据,不去做改数操作")
        return 0
#当前时间的前一天=跑批业务日期，才能正常申请借款
def update_batch_log():
    sql='select now();'
    date_time=DataBase(which_db).get_one(sql)
    d=str(date_time[0]+datetime.timedelta(days=-1))
    yudate=d[:4]+d[5:7]+d[8:10]
    sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
    BUSI_DATE=DataBase(which_db).get_one(sql2)
    if yudate==BUSI_DATE[0]:
        print("当前服务器日期为:",date_time[0])
        print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
    else:
        sql3="update sys_batch_log set BUSI_DATE='"+yudate+"' where BUSI_DATE='"+BUSI_DATE[0]+"';"
        DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).closeDB()

if __name__ == '__main__':
    compute_code('1234567890')