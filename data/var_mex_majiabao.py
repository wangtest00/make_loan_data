__all__=['host_api','host_action','host_mgt','head_api','host_pay','host_coll','head_mgt','head_pay','CONFIGS','prodNo','which_db','appNo','shenpiren']

appNo='201'    #当前产品号，测试201用多期，马甲包只支持单期
shenpiren={'201':['wangs2@whalekun.com','https://test-mgt.lanaplus.mx','28070110','mex_pdl_loan'],'202':['wangs@whalekun.com','https://test-mgt.feriarapida.mx','25002400','mex_pdl_loan']}
which_db=shenpiren[appNo][3]   #数据库库名
prodNo=shenpiren[appNo][2]     #产品编号
host_mgt=shenpiren[appNo][1]   #MGT域名
host_api="https://test-api.quantx.mx"        #APP
host_action="https://test-action.quantx.mx"  #埋点
host_pay="https://test-pay.quantx.mx"        #支付
host_coll="https://test-coll.quantx.mx"      #催收
head_api={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","x-auth-token": "Bearer" ,"accept-encoding": "gzip","content-length": "63","host":"test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": appNo }

head_mgt={"Host": host_mgt[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin":host_mgt,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_mgt,"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
head_pay={"Host": host_pay[8:],"Connection": "keep-alive","Content-Length": "55",
"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*","sec-ch-ua-mobile": "?0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
"Content-Type": "application/json;charset=UTF-8","Origin": host_pay,"Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors",
"Sec-Fetch-Dest": "empty","Referer": host_pay,"Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cookie": "language=zh"}
CONFIGS = {
    'mex_pdl_loan': {'host':'192.168.0.60','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'mex_pdl_loan'},
    'manage_need_loan': {'host':'13.235.214.155','port':3306, 'user': 'cs_wangs','password': 'cs_wangs!qw####','database': 'manage_need_loan'}
}