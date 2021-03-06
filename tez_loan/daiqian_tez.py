import random
import string
from tez_loan.heads_tez import *
from database.dataBase_tez import *
from data.var_tez_loan import *
from tez_loan.daihou_tez import *


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
    print(x)
    return x

def login_code(registNo):
    code=compute_code(registNo)
    data={"appName":"TezLoan","appNo":"301","appType":"10090001","code":code,"gaid":"04b0a543-4f1e-45b8-9e1b-1f99be85ceaa",
          "ipAddr":"","latitude":"","longitude":"","osVersion":"11","phoneType":"lenovo","registNo":registNo,"versionNo":"1.0.1"}
    r=requests.post(host_api+"/api/cust/login",data=json.dumps(data),headers=head_api,verify=False)
    c=r.json()
    print(c)
    m=[]
    if c!=0:
        m.append(c['data']['token'])
        m.append(c['data']['custNo'])
        return m
    else:
        return 0

def cert_auth(registNo,custNo,headt):
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num=str(random.randint(1000,9999))
    data={"appName":appName,"appNo":appNo,"birthDay":"1992-05-06","certNo":num+"4567"+num,"custFirstName":"wang","custLastName":"shuang",
          "custMiddleName":"mmmm","education":"10190006","educationValue":"Doctorate/PhD","marriage":"10050001","marriageValue":"Married",
          "panNo":""+st+num+"W","registNo":registNo,"sex":"10070004","useEmail":"370sdfghhhj@gmail.com","useLang":"90000001",
          "useLangValue":"English","custNo":custNo}
    r=requests.post(host_api+'/api/cust/auth/cert',data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)
    if t!=0:
        #m=json.loads(t['message'])#字符串转字典
        return t['data']['custNo']
    else:
        pass

def auth(registNo,custNo,headt):
    data1={"address":"werttyyew","addressName":"Arunachal Pradesh Anjaw","county":"10360002","custNo":custNo,
           "postCode":"552555","residenceType":"10840004","residenceTypeValue":"Company distribution","state":"10360000"}
    r1=requests.post(host_api+'/api/cust/auth/address',data=json.dumps(data1),headers=headt,verify=False)
    print(r1.json())
    data2={"appNo":"301","certType":"WORK","custNo":custNo,"registNo":registNo}
    r2=requests.post(host_api+'/api/cust/auth/query/single/info',data=json.dumps(data2),headers=headt,verify=False)
    print(r2.json())
    #工作认证
    data3={"cityValue":"Andaman and Nicobar Island Nicobar","county":"10000001","custNo":custNo,"employeeStatus":"10850001",
           "employeeStatusValue":"Salaried","monSalary":"10870005","monSalaryValue":"30,000-50,000","state":"10000000","unitName":"test"}
    r3=requests.post(host_api+'/api/cust/auth/work',data=json.dumps(data3),headers=headt,verify=False)
    print(r3.json())
    #其他联系人认证
    data4=[{"contactName":"test111111","custNo":custNo,"phoneNo":"8686512345","relation":"10110001","relationValue":"Father"},
          {"contactName":"test22222222","custNo":custNo,"phoneNo":"8686861234","relation":"10110003","relationValue":"Spouse"}]
    r4=requests.post(host_api+'/api/cust/auth/contact',data=json.dumps(data4),headers=headt,verify=False)
    print(r4.json())
#申请提现
def loan(registNo,custNo,headt):
    data={"appNo":appNo,"custNo":custNo,"registNo":registNo}
    r=requests.post(host_api+'/api/loan/apply',data=json.dumps(data),headers=headt,verify=False)
    t=r.json()
    print(t)
    return t['data']['loanNo']

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
    sql2="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum1+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070015', '100700151644565274220.png', '100700151644565274220.png', '10080001', '.png', '248831', '301/20220211/"+registNo+"/', 'https://test-tez-loan.s3.ap-south-1.amazonaws.com/301/20220211/8686862222/100700151644565274220.png', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql3="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum2+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070016', '100700161644565285532.png', '100700161644565285532.png', '10080001', '.png', '269185', '301/20220211/"+registNo+"/', 'https://test-tez-loan.s3.ap-south-1.amazonaws.com/301/20220211/8686862222/100700161644565285532.png', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql4="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum3+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070017', '100700171644565292459.png', '100700171644565292459.png', '10080001', '.png', '270091', '301/20220211/"+registNo+"/', 'https://test-tez-loan.s3.ap-south-1.amazonaws.com/301/20220211/8686862222/100700171644565292459.png', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    sql5="INSERT INTO cu_cust_file_dtl(`ID`, `REGIST_NO`, `CUST_NO`, `APP_NO`, `BUSI_TYPE`, `SAVE_ATT_NAME`, `UPLOAD_ATT_NAME`, `ATT_TYPE`, `ATT_FILE`, `ATT_SIZE`, `PH_PATH`, `IN_PATH`, `REMARK`, `INST_TIME`, `INST_USER_NO`, `UPDT_TIME`, `UPDT_USER_NO`) VALUES ('"+t+'b88f206222e0'+tnum4+"', '"+registNo+"', '"+custNo+"', '"+appNo+"', '10070004', '100700041644565333697.png', '100700041644565333697.png', '10080001', '.png', '269815', '301/20220211/"+registNo+"/', 'https://test-tez-loan.s3.ap-south-1.amazonaws.com/301/20220211/8686862222/100700041644565333697.png', NULL, '"+inst_time+"', 'sys', NULL, NULL);"
    DataBase(tez_db).executeUpdateSql(sql2)
    DataBase(tez_db).executeUpdateSql(sql3)
    DataBase(tez_db).executeUpdateSql(sql4)
    DataBase(tez_db).executeUpdateSql(sql5)
#绑定银行卡，需要把银行卡号改成明显错的，环境怕放出真实的钱   卡号不足9位就是提现失败，三方验证失败
def bank_auth(custNo,headt):
    bank_acct_no=str(random.randint(100000000,999999999))
    data={"bankAcctName":"wangmshuang","bankAcctNo":bank_acct_no,"bankAcctNoConfirm":bank_acct_no,"custNo":custNo,"ifscCode":"SBIN0001537"}
    r=requests.post(host_api+'/api/cust/auth/bank',data=json.dumps(data),headers=headt,verify=False)
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
    r=requests.post(host_api+"/api/loan/trial/instalment",data=data,headers=headt,verify=False)
    t=r.json()
    print(t)
    list=[]
    if t['data']['single'] is True:
        loanInstNums=str(t['data']['loanInstNums'])
        loanAmount=t['data']['loanAmount']
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
        data={"prodNo":prodNo,"custNo":custNo,"loanNo":loanNo,"loanAmt":loanAmt,"instNum":instNum}
        r=requests.post(host_api+"/api/trade/fin/less/withdraw",data=json.dumps(data),headers=headt,verify=False)
        print("api申请提现接口响应=",r.json())
        return 1


if __name__ == '__main__':
    i=['9207650013'
    ]
    for i in i:
        compute_code(i)