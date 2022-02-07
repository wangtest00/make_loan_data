import random,time,datetime
import requests,json,string
from make_loan_data.tez_loan.daihou_tez import *
from make_loan_data.public.dataBase_tez import *
from make_loan_data.data.var_tez_loan import *

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
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","accept-encoding": "gzip","content-length": "0","host": host_api[8:],
          "content-type": "application/json;charset=utf-8","version_no":"2.6.3","app_type":"10090001",
        "x-app-type": "10090001","app_no": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
    return head
def head_token_f(token):
    head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"multipart/form-data; boundary=65d7b53d-2308-466f-8b4a-42f32dd4a9f9","version_no":"2.6.3","app_type":"10090001",
          "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def head_token_w(token):
    head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
          "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"application/x-www-form-urlencoded","version_no":"2.6.3","app_type":"10090001",
          "app_no":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def login_code(registNo):
    code=compute_code(registNo)
    data={"appName":appName,"appNo":appNo,"appType":"10090001","code":code,"gaid":"12303937-ccde-46ee-a455-5146d36344dd",
          "ipAddr":"192.168.20.196","osVersion":"10","phoneType":"HUAWEI",
          "registNo":registNo,"utmCampaign":"","utmContent":"","utmMedium":"","utmSource":"","utmTerm":"","versionNo":"2.6.3"}
    r=requests.post(host_api+"/api/cust_info/cust/login?lang=en",data=json.dumps(data),headers=head_api,verify=False)
    c=r.json()
    print(c)
    if c!=0:
        token=c['data']['token']
        return token
    else:
        return 0

def cert_auth(registNo,headt):
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num=str(random.randint(1000,9999))
    data={"appName":appName,"appNo":appNo,"birthDay":"1999-05-06","certNo":num+"4566"+num,"custFirstName":"wang","custLastName":"shuang",
          "custMiddleName":"mmmm","education":"10190006","marriage":"10050001","panNo":""+st+num+"W","registNo":registNo,"sex":"10030001",
          "useEmail":"370sdfghhhj@gmail.com","useLang":"90000001"}
    r=requests.post(host_api+'/api/cust_india/cert/cert_auth?lang=en',data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)
    if t!=0:
        #m=json.loads(t['message'])#字符串转字典
        return t['data']['custNo']
    else:
        pass
def auth(registNo,custNo,headt):
    data1={"address":"wwsdddxx","county":"10010002","custNo":custNo,"postCode":"123456","residenceType":"10840005","state":"10010000"}
    r1=requests.post(host_api+'/api/cust_india/cert/save_address?lang=en',data=json.dumps(data1),headers=headt,verify=False)
    print(r1.json())
    data2={"appNo":appNo,"certType":"WORK","custNo":custNo,"registNo":registNo}
    r2=requests.post(host_api+'/api/cust_india/query/single_cust_auth?lang=en',data=json.dumps(data2),headers=headt,verify=False)
    print(r2.json())
    #工作认证
    data3={"custNo":custNo,"employeeStatus":"10850002","monSalary":"10870009"}
    r3=requests.post(host_api+'/api/cust_india/work/auth?lang=en',data=json.dumps(data3),headers=headt,verify=False)
    print(r3.json())
    #其他联系人认证
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
    DataBase(tez_db).executeUpdateSql(sql)
    sql2="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070015', '100700151627276671905.jpg', '100700151627276671905.jpg', '10080001', '.jpg', '918911', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700151627276671905.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070016', '100700161627276676407.jpg', '100700161627276676407.jpg', '10080001', '.jpg', '581306', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700161627276676407.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070017', '100700171627276682497.jpg', '100700171627276682497.jpg', '10080001', '.jpg', '569745', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700171627276682497.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql5="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum4+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070004', '100700041627276687389.jpg', '100700041627276687389.jpg', '10080001', '.jpg', '575899', '102/20210726/"+registNo+"/', 'https://qt-fpdl-app.s3.ap-south-1.amazonaws.com/102/20210726/"+registNo+"/100700041627276687389.jpg', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(tez_db).executeUpdateSql(sql2)
    DataBase(tez_db).executeUpdateSql(sql3)
    DataBase(tez_db).executeUpdateSql(sql4)
    DataBase(tez_db).executeUpdateSql(sql5)
#绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱
def bank_auth(custNo,headt):
    bank_acct_no=str(random.randint(100000000,999999999))
    data={"bankAcctName":"wangmmmmshuang","bankAcctNo":bank_acct_no,"custNo":custNo,"ifscCode":"SBIN0001537"}
    r=requests.post(host_api+'/api/cust_india/bank/bank_auth?lang=en',data=json.dumps(data),headers=headt,verify=False)
    print("绑卡认证接口响应=",r.json())
    sql="update cu_cust_bank_card_dtl set OPEN_ORG='QATEST' where cust_No='"+custNo+"';"#支付放款需要查询银行机构，临时update，正式提测，需要喊接口写入
    DataBase(tez_db).executeUpdateSql(sql)

#当前时间的前一天=跑批业务日期，才能正常申请借款
def update_Batch_Log():
    sql='select now();'
    date_time=DataBase(tez_db).get_one(sql)
    d=str(date_time[0]+datetime.timedelta(days=-1))
    yudate=d[:4]+d[5:7]+d[8:10]
    sql2='select BUSI_DATE from sys_batch_log order by BUSI_DATE desc limit 1;'
    BUSI_DATE=DataBase(tez_db).get_one(sql2)
    if yudate==BUSI_DATE[0]:
        print("当前服务器日期为:",date_time[0])
        print("当期系统跑批业务日期为:",BUSI_DATE[0],"无需修改批量日期")
    else:
        sql3="update sys_batch_log set BUSI_DATE='"+yudate+"',BATCH_STAT='10490002',IS_PROD_SEL='10000001' where BUSI_DATE='"+BUSI_DATE[0]+"';"
        DataBase(tez_db).executeUpdateSql(sql3)
    DataBase(tez_db).closeDB()

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

def withdraw(registNo,custNo,loanNo,headt,headw):
    trial_list=trial_instalment(loanNo,headw)
    if trial_list==0:
        print("未获取到期数和贷款金额,不调提现接口")
        return '未获取到期数和贷款金额,不调提现接口'
    else:
        instNum=trial_list[0]
        loanAmt=trial_list[1]
        data={"custNo":custNo,"instNum":instNum,"loanAmt":loanAmt,"loanNo":loanNo,"prodNo":prodNo}
        r=requests.post(host_api+"/api/trade/fin/less/withdraw?lang=en",data=json.dumps(data),headers=headt,verify=False)
        print("api申请提现接口响应=",r.json())
        return 1


if __name__ == '__main__':
    update_Batch_Log()