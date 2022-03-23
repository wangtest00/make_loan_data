from data.var_tez_loan import *

def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "en","accept-encoding": "gzip","content-length": "0","host": host_api[8:],
          "content-type": "application/json;charset=utf-8","X-App-Version":app_version_no,"X-App-Type":"10090001",
          "X-App-No": appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=d17x0ET9jFp5BBK_qidExJqVs5THhstLnVk2eMEH" }
    return head
def head_token_f(token):
    head={"user-agent":"Dart/2.12 (dart:io)","Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"multipart/form-data; boundary=65d7b53d-2308-466f-8b4a-42f32dd4a9f9","X-App-Version":app_version_no,"X-App-Type":"10090001",
          "X-App-No":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head
def head_token_w(token):
    head={"user-agent":"Mozilla/5.0 (Linux; U; Android 10; en; LIO-AL00 Build/HUAWEILIO-AL00) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1",
          "Accept-Language":"en","accept-encoding":"gzip","content-length":"277","host":host_api[8:],
          "content-type":"application/x-www-form-urlencoded","X-App-Version":app_version_no,"X-App-Type":"10090001",
          "X-App-No":appNo,"x-auth-token":'Bearer '+str(token),"Cookie":"JSESSIONID=ffUdZQ5pBRFudhsBmGLidri4nNB7GRSE4BieOKlY" }
    return head