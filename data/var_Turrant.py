__all__=['app_no','host_api','host_action','host_mgt','head_api','head_mgt','CONFIGS','prodNo','inter_db','head_pay','host_pay']

inter_db='manage_need_loan'
prodNo='10400001'
app_no='104'
host_api="https://test-appa.quantstack.in"
host_pay="https://test-pay.quantstack.in"
host_action="https://test-action.quantstack.in"
host_mgt="https://test-mgt.quantstack.in"
head_api={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","x-auth-token": "Bearer" ,"accept-encoding": "gzip","x-api":"1",
          "content-length": "63","host": "test-appa.quantstack.in","x-app-name": "Turrant","content-type": "application/json",
         "x-app-type": "10090001","x-app-version": "100","x-app-no": app_no }

head_mgt={"Host": "test-mgt.quantstack.in","Connection": "keep-alive","Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36","Content-Type": "application/json;charset=UTF-8","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": "https://test-mgt.quantstack.in/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}

head_pay={"Host":"test-pay.quantstack.in","Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
                "User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br"}

CONFIGS = {'manage_need_loan': {'host':'172.31.25.83','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}}