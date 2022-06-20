import json,requests
from database.dataBase_india import *
from data.var_tur import *
from turrant.daiQian import *
from public.check_api import *

#登录mgt,返回ssid值
def login_mgt():
    data={"loginName":mgtuser,"password":"jk@123"}
    r=requests.post(host_mgt+mgtLoginUrl,data=json.dumps(data),headers=head_mgt,verify=False)
    check_api(r)
    for item in r.cookies:
        pass
    return item.value

#注意：审批人员平均推单存储过程，只对空闲在线的审批人推单
##将审批人的审批状态为空闲： 空闲10460001   审批中10460002 离开10460003
def update_appr_user_stat():
    sql="update sys_user_info set APPR_USER_STAT='10460001',ON_LINE='10000001',IS_USE='10000001'  where user_no='"+mgtuser+"';"
    DataBase(configs).executeUpdateSql(sql)
#分配审批人员及审批通过-递归函数
def approve(loan_no):
    head=head_mgt_c()
    data1={"loanNos":[loan_no],"targetUserNo":mgtuser}
    r1=requests.post(host_mgt+'/api/approve/distribution/case?lang=zh',data=json.dumps(data1),headers=head,verify=False)  #1.分配审批人员
    check_api(r1)
    data2={"loanNo":loan_no,"decisionReason":"10280020","apprRemark":"test","approveResultType":"PASS"}
    r2=requests.post(host_mgt+'/api/approve/handle/approve?lang=zh',data=json.dumps(data2),headers=head,verify=False)#2.审批通过
    check_api(r2)
    t2=r2.json()
    if t2['errorCode']!=0:
        print("开始调用分单审批存储过程")
        DataBase(configs).call_4_proc()
        #return approve(loan_no)
    else:
        pass
#批量分配审批人员及审批通过
def pl_approve(loanNo):
    head=head_mgt_c()
    for loanNo in loanNo:
        data1 = {"loanNos": [loanNo], "targetUserNo": mgtuser}
        #1.分配审批人员
        r1 = requests.post(host_mgt + '/api/approve/distribution/case?lang=zh', data=json.dumps(data1), headers=head,verify=False)
        check_api(r1)
        data2={"loanNo":loanNo,"decisionReason":"10280038","apprRemark":"测试通过","riskLevel":"DEFAULT","riskScore":"0","approveResultType":"PASS"}
        #2.审批通过
        r2=requests.post(host_mgt+'/api/approve/handle/approve?lang=zh',data=json.dumps(data2),headers=head,verify=False)
        check_api(r2)
#组装header+用户登录cookie
def head_mgt_c():
    ssid=login_mgt()
    head={"Host": "test-mgt.quantstack.in","Connection": "keep-alive","Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8","Origin": "https://test-mgt.quantx.mx","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh; ssid="+ssid+"; hasLogin=1"}
    return head
def head_mgt_2():
    ssid=login_mgt()
    head2={"Host": "test-mgt.quantstack.in","Connection": "keep-alive","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
"Accept": "application/json, text/plain, */*",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh; ssid="+ssid+"; hasLogin=1"}
    return head2
#批量分配及审批
def pl_shenpi():
    head=head_mgt_2()
    r=requests.get(host_mgt+'/api/approve/distribution/list?pageSize=10&pageNum=1&lang=zh',headers=head,verify=False)
    t=r.json()
    t=t['list']
    loan_No_List=[]
    for i in range(len(t)):
        if t[i]['apprStat']=='10200003':
            if t[i]['apprUserNo']=='wangs2@whalekun.com' or t[i]['apprUserNo']=='liull@quantditech.com' or t[i]['apprUserNo']=='lijiahui' or t[i]['apprUserNo']=='wangs@whalekun.com':
                loan_no=t[i]['loanNo']
                loan_No_List.append(loan_no)
    if len(loan_No_List)==0:
        print("无需审批")
    else:
        print(loan_No_List)
        pl_approve(loan_No_List)

if __name__ == '__main__':
    #approve('L1042206028220528284115599360')
    pl_shenpi()