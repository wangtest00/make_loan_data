from make_loan_data.data.var_tez_loan import *

def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","accept-encoding": "gzip","content-length": "0","host": host_api[8:],
          "content-type": "application/json;charset=utf-8","X-App-Version":"1.0.0","X-App-Type":"10090001",
          "X-App-No": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
    return head
def head_token_f(token):
    head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"multipart/form-data; boundary=65d7b53d-2308-466f-8b4a-42f32dd4a9f9","X-App-Version":"1.0.0","X-App-Type":"10090001",
          "X-App-No":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def head_token_w(token):
    head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
          "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"application/x-www-form-urlencoded","X-App-Version":"1.0.0","X-App-Type":"10090001",
          "X-App-No":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head

def head_zhanqi(token):
    head={"authority": "test-api.quantx.mx",
    "method": "POST",
    "path": "/api/h5/repay",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-length": "223",
    "content-type": "application/json",
    "origin": "https://test-repay.lanaplus.mx",
    "referer": "https://test-repay.lanaplus.mx/",
    "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "x-app-name": "lanaplus",
    "x-app-no": "201",
    "x-app-type": "10090003",
    "x-app-version": "2.0.0",
    "x-auth-token": "Bearer "+token,
    "x-user-language":"en"}
    return head