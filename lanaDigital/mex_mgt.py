from lanaDigital.daiqian import *
from data.var_mex_credit import *
import requests,json


def check_api(r):
    try:
        if r.status_code==200:
            t=r.json()
            if t['errorCode']==0:
                print("校验正确，接口返回=",t)
                return t
            else:
                print("校验错误，接口返回=",t)
                return 0
        else:
            print("环境可能不稳定，接口返回=",r.content)
            return 0
    except Exception as e:
        print("捕获到异常：",e)
        return 0
#登录mgt接口,返回ssid值
def login_mgt():
    data={"loginName":user[0],"password":"jk@123"}
    r=requests.post(host_mgt+'/api/login/auth?lang=en&lang=zh',data=json.dumps(data),headers=head_mgt,verify=False)
    check_api(r)
    for item in r.cookies:
        print(item.name,item.value)
    return item.value

#注意：审批人员平均推单存储过程，只对空闲在线的审批人推单
##将审批人的审批状态为空闲： 空闲10460001 ,审批中10460002 离开10460003
def update_appr_user_stat():
    sql="update sys_user_info set APPR_USER_STAT='10460001',ON_LINE='10000001',IS_USE='10000001'  where user_no='"+user[0]+"';"
    DataBase(which_db).executeUpdateSql(sql)

#分配审批人员及审批通过接口
def approve(custNo):
    head=head_mgt_c()
    r=requests.get(host_mgt+"/api/approve/distribution/list?pageSize=10&pageNum=1&lang=zh",headers=head,verify=False)
    t=r.json()
    list=t['list']
    for list in list:
        #print(list)
        if  list['custNo']==custNo:
            flowId=list['flowId']
            data1={"flowIds":[flowId],"targetUserNo":user[0]}
            r=requests.post(host_mgt+'/api/approve/distribution/case?lang=zh',data=json.dumps(data1),headers=head,verify=False)  #1.分配审批人员
            check_api(r)
            data2={"flowId":flowId,"decisionReason":"10280038","apprRemark":"test for approve","approveResultType":"PASS"}
            r=requests.post(host_mgt+'/api/approve/handle/approve?lang=zh',data=json.dumps(data2),headers=head,verify=False)#2.审批通过
            check_api(r)
            print("该笔案件-审批通过")
        else:
            print("该笔授信案件不是该客户的")
            pass

#组装header+用户登录cookie
def head_mgt_c():
    ssid=login_mgt()
    head={"Host": "test-mgt.lanadigital.mx","Connection": "keep-alive","Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8","Origin": "https://test-mgt.lanadigital.mx","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": "https://test-mgt.lanadigital.mx/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh; ssid="+ssid+"; hasLogin=1"}
    return head
def head_mgt_2():
    ssid=login_mgt()
    head2={"Host": "test-mgt.lanadigital.mx","Connection": "keep-alive","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
"Accept": "application/json, text/plain, */*","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty","Referer": "https://test-mgt.lanadigital.mx/","Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh; ssid="+ssid+"; hasLogin=1"}
    return head2

def pl_approve(head):
    r=requests.get("https://test-mgt.lanadigital.mx/api/approve/flow/list?pageSize=10&pageNum=1&params[registNo]=&lang=zh",headers=head,verify=False)
    t=r.json()
    s=t['list']
    for i in range(len(s)):
        flowId=s[i]['flowId']
        data1={"flowIds":[flowId],"targetUserNo":user[0]}
        r=requests.post(host_mgt+'/api/approve/distribution/case?lang=zh',data=json.dumps(data1),headers=head,verify=False)  #1.分配审批人员
        check_api(r)
        #data2={"flowId":flowId,"decisionReason":"10280038","apprRemark":"test for approve","approveResultType":"PASS"}#2.审批通过
        data2={"flowId":flowId,"decisionReason":"10280024","apprRemark":"test for approve","approveResultType":"REJECT"}#3.审批拒绝
        r=requests.post(host_mgt+'/api/approve/handle/approve?lang=zh',data=json.dumps(data2),headers=head,verify=False)
        check_api(r)
        print("该笔案件-审批通过")

def pl_shenpi():
    head=head_mgt_c()
    pl_approve(head)

if __name__ == '__main__':
    approve('C2082111038144131744472432640')
    #pl_shenpi()
