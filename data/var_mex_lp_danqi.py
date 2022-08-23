
appNo = '201'
mainInfo = {'201': ['wangs_danqi@whalekun.com', 'https://test-mgt.lanaplus.mx', '25002400', 'mex_pdl_loan', 'LanaPlus','FC423D8F-BC7E-4430-BD97-66E903DANQI', '140', '10090001'],
            '202': ['wangs@whalekun.com', 'https://test-mgt.feriarapida.mx', '25002400', 'mex_pdl_loan', 'FeriaRapida']}
which_db = mainInfo[appNo][3]  # 数据库库名
prodNo = mainInfo[appNo][2]  # 产品编号
host_mgt = mainInfo[appNo][1]  # MGT域名
app_type = mainInfo[appNo][7]  # app类型：IOS=10090002   Android=10090001
host_api = "https://test-api.quantx.mx"        # API
host_action="https://test-action.quantx.mx"    # 埋点
host_pay =  "https://test-pay.quantx.mx"       # 支付
head_digt_pay="https://test-digital-payment.quantx.mx" #支付平台
host_coll = "https://test-collection.lanaplus.mx"      #催收

head_api = {"user-agent": "Dart/2.12 (dart:io)", "x-user-language": "es", "x-auth-token": "Bearer","accept-encoding": "gzip", "content-length": "63", "host": "test-api.quantx.mx","x-app-name": mainInfo[appNo][4],"content-type": "application/json", "x-app-type": app_type, "x-app-version": mainInfo[appNo][6],"x-app-no": appNo}
head_mgt = {"Host": host_mgt[8:], "Connection": "keep-alive", "Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*", "sec-ch-ua-mobile": "?0","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8", "Origin": host_mgt, "Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty", "Referer": host_mgt, "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9", "Cookie": "language=zh"}
head_pay = {"Host": host_pay[8:], "Connection": "keep-alive", "Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*", "sec-ch-ua-mobile": "?0","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8", "Origin": host_pay, "Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty", "Referer": host_pay, "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9", "Cookie": "language=zh"}
head_digt_pay = {"Host": head_digt_pay[8:], "Connection": "keep-alive", "Content-Length": "55","sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',"Accept": "application/json, text/plain, */*", "sec-ch-ua-mobile": "?0","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36","Content-Type": "application/json;charset=UTF-8", "Origin": head_digt_pay, "Sec-Fetch-Site": "same-origin","Sec-Fetch-Mode": "cors","Sec-Fetch-Dest": "empty", "Referer": head_digt_pay, "Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9", "Cookie": "language=zh"}

configs= {'host': '192.168.0.60', 'port': 3306, 'user': 'cs_wangs', 'password': 'cs_wangs!qw####','database': 'mex_pdl_loan'}