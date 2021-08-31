__all__=['india_api','host2','india_mgt','head_api','head_mgt','CONFIGS','india_prodNo','inter_db','head_india_pay']

inter_db='manage_need_loan'
india_prodNo='5'
india_api="http://api-test.quantstack.in"
host2="https://test-action.quantstack.in"
india_mgt="http://test-mgt.quantstack.in/"
head_api={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","x-auth-token": "Bearer" ,"accept-encoding": "gzip","content-length": "63","host": "test-api.quantstack.in","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201" }

head_mgt={"Host": "test-mgt.quantstack.in","Connection": "keep-alive","Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": "http://test-mgt.quantstack.in/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}

head_india_pay={"Host":"test-pay.quantstack.in","Connection":"keep-alive","Content-Length":"116","Postman-Token":"68cc47f6-8c1f-4ebd-a929-b1ae10b7dd19",
                "User-Agent":"PostmanRuntime/7.28.2","Accept":"*/*","Content-Type":"application/json","Accept-Encoding":"gzip, deflate, br"}

CONFIGS = {'manage_need_loan': {'host':'13.235.214.155','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}}
india_prodNo=india_prodNo
india_api=india_api
host2=host2
india_mgt=india_mgt
head_api=head_api
head_mgt=head_mgt
CONFIGS=CONFIGS
inter_db=inter_db
head_india_pay=head_india_pay