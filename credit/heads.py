from make_loan_data.data.var_mex_credit import *

def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "0","host_api": host_api[8:],"x-app-name": "LanaDigital","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "1.0.0","x-app-no": appNo,"x-auth-token":'Bearer '+str(token) }
    return head
def head_token2(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es" ,"accept-encoding": "gzip","content-length": "63","host_api": "test-action.lanadigital.mx","x-app-name": "LanaDigital","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "1.0.0","x-app-no":appNo,"x-auth-token":'Bearer '+str(token) }
    return head
def head_token_kyc(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "63","host_api": "test-api.lanadigital.mx","x-app-name": "LanaDigital","content-type": "multipart/form-data; boundary=--dioBoundary&Happycoding-1538342764",
        "x-app-type": "10090001","x-app-version": "1.0.0","x-app-no": appNo,"x-auth-token":'Bearer '+str(token) }
    return head