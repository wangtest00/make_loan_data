__all__=['host_api','host_action','host_mgt','head_api','host_pay','host_coll','head_mgt','head_pay','CONFIGS','which_db','appNo','user']

appNo='208'
which_db='mex_credit'
user=['wangs2@whalekun.com']
host_api="https://test-api.lanadigital.mx"         #APP接口
host_action="https://test-action.lanadigital.mx"   #埋点
host_mgt="https://test-mgt.lanadigital.mx"         #MGT
host_pay="https://test-pay.lanadigital.mx"         #支付
host_coll="https://test-coll.lanadigital.mx"       #催收

head_api={"user-agent": "okhttp/4.9.1","x-user-language": "es","x-auth-token": "Bearer" ,"accept-encoding": "gzip","content-length": "25","host": host_api[8:],
          "x-app-name": "LanaDigital","content-type": "application/json;charset=utf-8","x-app-type": "10090001","x-app-version": "1.0.0","x-app-no": appNo }

head_mgt={"Host": host_mgt[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.54 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": host_mgt,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_mgt,"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}

head_pay={"Host": host_pay[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": host_pay,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_pay,"Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
CONFIGS = {
    'mex_credit': {'host':'192.168.0.60','port':3306, 'user': 'cs_liull','password': 'cs_liull!qw####','database': 'mex_credit'},
}
