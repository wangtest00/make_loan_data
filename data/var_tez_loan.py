__all__=['host_api','host_mgt','host_pay','head_api','head_mgt','head_pay','CONFIGS','prodNo','appNo','appName','inter_db']

inter_db='manage_need_loan'
prodNo_tez=['5','102','ZET_LOAN']
prodNo=prodNo_tez[0]
appNo=prodNo_tez[1]
appName=prodNo_tez[2]
host_api="http://192.168.20.112:8082"
host_pay="https://test-pay.quantstack.in"
host_mgt="https://test-mgt.quantstack.in"
head_api={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","x-auth-token": "Bearer" ,"accept-encoding": "gzip","content-length": "63","host": host_api[8:],"x-app-name": appName,"content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": appNo }

head_mgt={"Host": host_mgt[8:],"Connection": "keep-alive","Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36","Content-Type": "application/json;charset=UTF-8","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_mgt,"Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}

head_pay={"Host":host_pay[8:],"Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
                "User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br"}

CONFIGS = {'manage_need_loan': {'host':'172.31.25.83','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}}