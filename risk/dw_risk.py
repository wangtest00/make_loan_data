import pymysql
import requests,json
from data.var_mex_lp_duoqi import *
from database.dataBase_mex import *
#生成下载地址
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
#文件下载地址
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

#调用对外风控接口测试,暂时屏蔽签名20220511
def openapi_service_risk_score(url):
    head={"Content-Type":"application/json",
		  "x-access-key-id":"HQLNTJFY7WO9WB+3MCD1",  #商户key，暂时写死
          "x-request-time": "202205131T014805-0500", #获得该值，需要去调SignMain类main方法，python暂时不调jar包
          "x-signature":"34e4415c7db28567968680566b2aa7ba83e159557645f4f9b83e362fc0170084",}#获得该值，需要去调SignMain类main方法，python暂时不调jar包
    data={"params":
		{           "applyTm": "2022-05-11 01:26:14",
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
					"custType": "1",
					"custNo": "C2012205108212268995555033088",
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
						"cuTotOvduTms": "0",
						"firstDisbrLoan": "L2012205108212269092724473856",
						"lastSettleLoan": "L2012205108212269092724473856",
						"lastApplyTime": "2022-05-10 02:29:02",
						"lastDisbrTime": "2022-05-10 02:29:40",
						"lastDueDate": "2022-05-17",
						"lastSettleTime": "2022-05-10 02:29:50",
						"lastProdNo": "28080070200",
						"lastApprAmt": 1500.00,
						"lastPrinAmt": 1500.00,
						"lastDisbrAmt": 1500.00,
						"lastLoanRank": "1",
						"lastOvduDays": "0"
					        },
					"loanNo": "L2012205118212615679862571008",
					"msg":url[2],
					"phoneNo": "8278085774"
					    },
		"serviceProdNo": "WK122300_666_Reloan_OwnRules"#决策产品名
		}
    print(data)
    r=requests.post('http://k8s-test1mex-elbtestm-2844e16dc9-384f1fecec492805.elb.us-west-1.amazonaws.com:8080/openapi/service/risk_score',data=json.dumps(data),headers=head)
   #生产地址
    #r=requests.post('http://54.176.19.126:8182/openapi/service/risk_score',data=json.dumps(data),header=header)
    print(r.json())

if __name__ == '__main__':
    #pre_sign_url('201/20220408/5553331111/11090004_1649397208286.json')
    url=downloadUrl('C2012205108212268995555033088')
    openapi_service_risk_score(url)