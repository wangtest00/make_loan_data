from make_loan_data.data.var_mex_lp_danqi import *

def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "0","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": app_type,"x-app-version": "116","x-app-no": appNo,"x-auth-token":'Bearer '+str(token) }
    return head
def head_token2(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es" ,"accept-encoding": "gzip","content-length": "63","host_api": "test-action.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": app_type,"x-app-version": "116","x-app-no":appNo,"x-auth-token":'Bearer '+str(token) }
    return head
def head_token_kyc(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "63","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "multipart/form-data; boundary=--dioBoundary&Happycoding-1538342764",
        "x-app-type": app_type,"x-app-version": "116","x-app-no": appNo,"x-auth-token":'Bearer '+str(token) }
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