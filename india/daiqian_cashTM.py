import json
import random
import requests
import string
from data.var_india import *


def check_api(r):
    try:
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
    except Exception as e:
        print("捕获到异常：",e)
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
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "0","host": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201","x-auth-token":'Bearer '+token }
    return head
def login_code(registNo):
    code=compute_code(registNo)
    data={"appName":"CashTM","appNo":"102","appType":"10090001","code":code,"gaid":"12303937-ccde-46ee-a455-5146d36344dd","ipAddr":"192.168.20.223","osVersion":"10","phoneType":"vivo",
          "registNo":registNo,"utmCampaign":"","utmContent":"","utmMedium":"","utmSource":"","utmTerm":"","versionNo":"2.6.2"}
    r=requests.post(host+"/api/cust_info/cust/login?lang=en",data=json.dumps(data),headers=head_api,verify=False)
    print(r.json())
    try:
        c=check_api(r)
        if c!=0:
            t=r.json()
            token=t['token']
            return token
        else:
            return 0
    except Exception as e:
        print(e)
        return 0
def cert_auth(registNo):
    st=''
    for j in range(5):  #生成5个随机英文大写字母
        st+=random.choice(string.ascii_uppercase)
    num=str(random.randint(1000,9999))
    data={"appName":"CashTM","appNo":"102","birthDay":"1999-05-06","certNo":"122345666666","custFirstName":"wang","custLastName":"shuang","custMiddleName":"mimi","education":"10190006",
          "marriage":"10050001","panNo":""+st+num+"W","registNo":registNo,"sex":"10030001","useEmail":"sdfghhhj@gmail.com","useLang":"90000001"}
    r=requests.post(host+'/api/cust_india/cert/cert_auth?lang=en',data=json.dumps(data),headers=head_api)
    t=check_api(r)
    if t!=0:
        t=json.loads(t['message'])#字符串转字典
        return t['custNo']
    else:
        pass
def auth(registNo,custNo,headt):
    data1={"address":"wwsdddxx","county":"10010002","custNo":custNo,"postCode":"123456","residenceType":"10840005","state":"10010000"}
    r1=requests.post(host+'/api/cust_india/cert/save_address?lang=en',data=json.dumps(data1),headers=headt)
    check_api(r1)
    data2={"appNo":"102","certType":"WORK","custNo":custNo,"registNo":registNo}
    r2=requests.post(host+'/api/cust_india/query/single_cust_auth?lang=en',data=json.dumps(data2),headers=headt)
    print(r2.json())
    data3={"custNo":custNo,"employeeStatus":"10850002","monSalary":"10870009"}
    r3=requests.post(host+'/api/cust_india/work/auth?lang=en',data=json.dumps(data3),headers=headt)
    check_api(r3)
    data4=[{"contactName":"wang","custNo":custNo,"phoneNo":"6666677777","relation":"10110001"},{"contactName":"ye","custNo":custNo,"phoneNo":"5555566666","relation":"10110006"}]
    r4=requests.post(host+'/api/cust_india/contact/auth?lang=en',data=json.dumps(data4),headers=headt)
    check_api(r4)
#申请提现
def loan(registNo,custNo,headt):
    data={"appNo":"102","custNo":custNo,"registNo":registNo}
    r=requests.post(host+'/api/loan_india/start?lang=en',data=json.dumps(data),headers=headt)
    t=r.json()
    print(t['loanNo'])
    return t

if __name__ == '__main__':
    # registNo=str(random.randint(8000000000,9999999999)) #10位随机数
    # token=login_code(registNo)
    # custNo=cert_auth(registNo)
    # headt=head_token(token)
    # auth(registNo,custNo,headt)
    # loan(registNo,custNo,headt)
    c=compute_code('7428089716')
    print(c)