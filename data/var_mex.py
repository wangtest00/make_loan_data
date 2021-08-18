__all__=['host_api','host_action','host_mgt','head_api','host_pay','host_coll','head_mgt','head_pay','CONFIGS','prodNo','which_db']

which_db='mex_pdl_loan'
prodNo='81002021'  #81002021多期   71002021单期
host_api="http://test-api.quantx.mx"         #APP
host_action="https://test-action.quantx.mx"  #埋点
host_mgt="https://test-mgt.quantx.mx"        #MGT
host_pay="https://test-pay.quantx.mx"        #支付
host_coll="https://test-coll.quantx.mx"      #催收
head_api={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","x-auth-token": "Bearer" ,"accept-encoding": "gzip","content-length": "63","host": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201" }

head_mgt={"Host": "test-mgt.quantx.mx","Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": "https://test-mgt.quantx.mx","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": "https://test-mgt.quantx.mx/","Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
head_pay={"Host": "test-pay.quantx.mx","Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": "https://test-pay.quantx.mx","Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": "https://test-pay.quantx.mx/","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
CONFIGS = {
    'mex_pdl_loan': {'host':'192.168.0.60','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'mex_pdl_loan'},
    'manage_need_loan': {'host':'13.235.214.155','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}
}
prodNo=prodNo
host_api=host_api
host_action=host_action
host_mgt=host_mgt
host_pay=host_pay
head_api=head_api
host_coll=host_coll
head_mgt=head_mgt
head_pay=head_pay
CONFIGS=CONFIGS
which_db=which_db