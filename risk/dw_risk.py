import pymysql
import requests,json
from data.var_mex_lp_duoqi import *
from database.dataBase import *

def pre_sign_url(objectKey):
    data={
    "bucketName":"test-mex-pdl", #生产环境需要改成生产桶名
    "objectKey":objectKey,
    "expiration":60}
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "0","content-type": "application/json", }
    r=requests.post("http://k8s-test1mex-elbtestm-2844e16dc9-384f1fecec492805.elb.us-west-1.amazonaws.com:8080/api/service/pre_sign_url",data=json.dumps(data),headers=head)
    t=r.json()
    downloadUrl=t['data']['downloadUrl']
    #print(downloadUrl)
    return downloadUrl

def downloadUrl(cust_no):
    applist=[]
    urllist=[]
    sql1="select path from lo_address_book_file_dtl where CUST_NO='"+cust_no+"';" #通讯录
    path1=DataBase(which_db).get_one(sql1)
    sql2="select path from lo_applist_file_dtl where CUST_NO='"+cust_no+"';"#applist
    path2 = DataBase(which_db).get_one(sql2)
    sql3="select FILE_PATH from lo_loan_msg_dtl where CUST_NO='"+cust_no+"';"#msg
    path3 = DataBase(which_db).get_one(sql3)
    applist.append(path1[0])
    applist.append(path2[0])
    applist.append(path3[0])
    #print(applist)
    url0=pre_sign_url(applist[0])
    url1=pre_sign_url(applist[1])
    url2=pre_sign_url(applist[2])
    urllist.append(url0)
    urllist.append(url1)
    urllist.append(url2)
    print(urllist)    #数据有错需要检查url是否能正常下载json文件
    return urllist

def openapi_service_risk_score(url):
    header={"x-access-key-id":"HQLNTJFY7WO9WB+3MCD1",  #商户key，暂时写死
            "x-request-time": "202204119T101123+0800", #获得该值，需要去调SignMain类main方法，python暂时不调jar包
            "x-signature":"ca24dc8bc0b0d6f283aaad4e717e9a61394307fabd691222d9263b08989e43b8"}#获得该值，需要去调SignMain类main方法，python暂时不调jar包
    data={    "params": {
					"applyTm": "2022-04-25 21:50:51",
					"appNo": "W101",    #目前该商户写死W101
					"appList": url[1],
					"basicInfo": {
					"birthday": "1972-12-23",
					"bankAcctNo": "002694904317618956",
					"custName": "HORACIO ISRAEL",
					"curpNo": "CAGH721223HDFRRR06",
					"contactPhone1": "9304895920",
					"contactName1": "Jack",
					"contactRelation1": "1",
					"contactPhone2": "9304855920",
					"contactName2": "Bob",
					"contactRelation2": "2",
					"gender": "0",
					   },
					"custType": "0",
					"custNo": "C2012203308197711149362511872",
					"contacts":url[0],
					"device": {
					"androidID": "df2b52a027dfa675",
					"appVersion": "1.0.0",
					"gaid": "2258bf96-8d7d-4830-b242-3fa0ba8a8ee2",
					"imei": "81e56989-8979-49a9-a93c-36c19ef8e9c7",
					"ipAddress": "10.206.39.92",
					"longitude": "-100.4070277",
					"latitude": "25.4070277",
					"mobileBrand": "Huawei",
					"mobileModel": "Huawei P40 Pro",
					"oSVersion": "10"},
					"historyLoan": {
					"cuTotOvduTms": "1",
					"firstDisbrLoan": "L2012204288207969151659212800",
					"lastSettleLoan": "L2012203308197711259718844416",
					"lastApplyTime": "2021-01-02 21:50:51",
					"lastDisbrTime": "2021-01-02 21:50:51",
					"lastDueDate": "2021-01-02",
					"lastSettleTime": "2021-01-02 21:50:51",
					"lastProdNo": "373007072000",
					"lastApprAmt": 2200.00,
					"lastPrinAmt": 2000.00,
					"lastDisbrAmt": 1400.00,
					"lastLoanRank": "3",
					"lastOvduDays": "-2"
					        },
					"loanNo": "L2012204288207969151659212800",
					"msg":url[2],
					"phoneNo": "7491564079"
					    },
					"serviceProdNo": "WK122300_666_Reloan_OwnRules"#决策产品名
					}
    r=requests.post('http://k8s-test1mex-elbtestm-2844e16dc9-384f1fecec492805.elb.us-west-1.amazonaws.com:8080/openapi/service/risk_score',data=json.dumps(data),header=header)
   #生产地址
    #r=requests.post('http://54.176.19.126:8182/openapi/service/risk_score',data=json.dumps(data),header=header)
    print(r.json())

if __name__ == '__main__':
    #pre_sign_url('201/20220408/5553331111/11090004_1649397208286.json')
    downloadUrl('C2012204288208221576399880192')