import string,requests,json,datetime
from make_loan_data.public.dataBase import *
from make_loan_data.lanaPlus.gaishu import *
from make_loan_data.lanaPlus.mex_mgt_lp import *
from make_loan_data.lanaPlus.heads import *
from make_loan_data.public.check_api import *
from make_loan_data.data.var_mex_lp import *
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
#1.第一个页面，注册认证，获得custNo
def auth_cert(registNo,headt):
    st=''
    for j in range(4):  #生成4个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    data={"birthdate":"1999-5-18","civilStatus":"10050001","curp":st+"990518MM"+st+"V8","delegationOrMunicipality":"zxcvbbbccxxx","education":"10190005",
          "fatherLastName":"SHUANG","gender":"10030001",
          "motherLastName":"TEST","name":"AUTO","outdoorNumber":"qweetyyu","phoneNo":registNo,"postalCode":"55555","state":"11130001","street":"444444","suburb":"asdfhhj","email":""}
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
    imei='a2eff92b-86cb-6666-a66c-84ae322f3adc'
    #设备信息
    data4={"appNo":appNo,"phoneNo":registNo,"dataType":"11090003","pageGet":"10000001","recordTime":"1621332187810","grabData":{"ipAddress":"2409:8162:a46:5405:1:0:107f:acec%20","ipResolveCit":"2409:8162:a46:5405:1:0:107f:acec%20",
    "ipResolveCom":"2409:8162:a46:5405:1:0:107f:acec%20","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":imei,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"抓取设备数据","recordTime":"1621332187810","userId":custNo,"mobileBrand":"HUAWEI","mobileModel":"LIO-AL00","systemVersion":"10","otherInfo":"274b98eb5c8aed06"},"custNo":custNo}
    #联系人
    data5={"appNo":appNo,"phoneNo":registNo,"dataType":"11090002","pageGet":"10000001","recordTime":"1621332187811","grabData":{"data":
    [{"contactName":"test","contactNo":"888 845 5666","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":imei,
      "mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取","recordTime":"1621332187811","userId":custNo},{"contactName":"test2","contactNo":"888 335 5777",
    "deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":imei,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"联系人列表抓取",
    "recordTime":"1621332187811","userId":custNo}]},"custNo":custNo}
    #短信内容
    data6={"appNo":appNo,"phoneNo":registNo,"dataType":"11090005","pageGet":"10000001","recordTime":"1621332187836","grabData":{"data":[{"body":"【中国农业银行】您尾号8579账户05月18日17:02完成支付宝交易人民币-5000.00，余额9999999999.19。","address":"95599","date":"2021-05-18 17:02:48.863","dateSent":"2021-05-18 17:02:46.000","sender":"95599","kind":"SmsMessageKind.Received"}]},"custNo":custNo}
    #设备信息
    data7={"appNo":appNo,"phoneNo":registNo,"dataType":"11090004","pageGet":"10000001","recordTime":"1621332187838","grabData":{"latitude":"30.550366","longitude":"104.062236","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":imei,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"11000003","recordTime":"1621332187838","userId":custNo},"custNo":custNo}
    #已安装应用
    data8={"appNo":appNo,"phoneNo":registNo,"dataType":"11090001","pageGet":"10000001","recordTime":"1621332187731","grabData":{"data":[{"appName":"安全教育平台","appPackage":"com.jzzs.ParentsHelper","appVersionNo":"1.7.0","deviceId":"a2eff92b-86cb-4614-a66c-84ae322f3adcA2:B4:74:63:FB:40LIO-AL00","imei":imei,"installTime":1599480832637,"lastUpdateTime":1618934047038,"mac":"A2:B4:74:63:FB:40","phoneNo":registNo,"recordBehavior":"App列表抓取","recordTime":"1621332187731","userId":custNo}]},"custNo":custNo}
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
    sql2="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070001', '100700011632400318577.jpg', '100700011632400318577.jpg', NULL, '.jpg', '677710', '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070002', '100700021632400319381.jpg', '100700021632400319381.jpg', NULL, '.jpg', '704805',  '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO `mex_pdl_loan`.`cu_cust_file_dtl`(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"','"+appNo+"', '10070004', '100700041632400322001.jpg', '100700041632400322001.jpg', NULL, '.jpg', '206389',  '"+appNo+"/20210923/4567891230/', NULL, NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(which_db).executeUpdateSql(sql2)
    DataBase(which_db).executeUpdateSql(sql3)
    DataBase(which_db).executeUpdateSql(sql4)
#绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱
def bank_auth(custNo,headt):
    bank_acct_no=str(random.randint(1000000,9999999))
    data={"bankCode":"10020037","clabe":"138455214411441118","custNo":custNo}
    r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt)
    check_api(r)
    time.sleep(1)                                         #改为6位随机数
    sql="update cu_cust_bank_card_dtl set BANK_ACCT_NO='"+bank_acct_no+"' where CUST_NO='"+custNo+"';"#修改成随机卡号，避免触发绑卡被拒:同一张银行卡不能被超过2个人绑定并放款成功
    DataBase(which_db).executeUpdateSql(sql)
#提现接口-app点击提现按钮
def withdraw(registNo,custNo,loan_no,headt):
    r=requests.get(host_api+'/api/loan/latest/'+registNo,headers=headt)#获取最近一笔贷款贷款金额，注意请求头content-length的值。The request body did not contain the specified number of bytes. Got 0, expected 63
    check_api(r)
    t=r.json()
    print('产品配置长度=',len(t['data']['trailPaymentDetail']))
    if t['errorCode']==0:
        loanAmt=t['data']['trailPaymentDetail'][0]['loanAmt']
        instNum=t['data']['trailPaymentDetail'][0]['instNum']
        data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loan_no,"prodNo":prodNo}
        r2=requests.post(host_api+'/api/trade/fin/confirm/withdraw',data=json.dumps(data),headers=headt)
        check_api(r2)
        return 1
    else:
        print("待提现页面，未获取到最近一笔贷款的数据,不去做改数操作")
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
#获取所有账单日
def getRepayDateList(registNo,headt):
    r=requests.get(host_api+'/api/loan/latest/'+registNo,headers=headt)#获取最近一笔贷款贷款金额，注意请求头content-length的值。The request body did not contain the specified number of bytes. Got 0, expected 63
    check_api(r)
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

def repay(custNo,loanNo,repayDate,headt):                                               #OXXO用CONEKTA
    data={"advance":"10000000","custNo":custNo,"defer":False,"loanNo":loanNo,"paymentMethod":"STP","repayDateList":[repayDate],"tranAppType":"Android"}
    r=requests.post(host_api+'/api/trade/fin/repay',data=json.dumps(data),headers=headt)
    m=check_api(r)
    repayList=[]
    if m!=0:
        t=r.json()
        transAmt=t['data']['stpRepayment']['transAmt']  #获取待还金额
        print(transAmt)
        repayList.append(transAmt)
    else:
        pass
    sql="select IN_ACCT_NO from pay_tran_dtl t where LOAN_NO='"+loanNo+"' and tran_use='10330002' and IN_ACCT_ORG='10020069' and TRAN_CHAN_NAME='STP支付渠道';"
    in_acct_no=DataBase(which_db).get_one(sql)
    in_acct_no=in_acct_no[0]
    if in_acct_no==None:
        print("repay接口请求有错，未向pay_tran_dtl表写入还款账号等数据",in_acct_no)
    else:
        print("repay接口请求正确，向pay_tran_dtl表写入还款账号等数据",in_acct_no)
        repayList.append(in_acct_no)
    return repayList
#提现接口-app点击提现按钮
def single_withdraw(registNo,custNo,loan_no,headt):
    loanAmt="1100.00"
    instNum='3'
    data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loan_no,"prodNo":prodNo}
    r=requests.post(host_api+'/api/trade/fin/withdraw',data=json.dumps(data),headers=headt)
    print(r.json())

def cx_beforeStat_afterStat(loanNo):
    sql='''select BEFORE_STAT,AFTER_STAT from lo_loan_dtl where LOAN_NO="'''+loanNo+'''";'''
    stat=DataBase(which_db).get_one(sql)
    return stat
if __name__ == '__main__':
    t=compute_code('9361866626')
    print(t)
    #login_pwd('8585852222')