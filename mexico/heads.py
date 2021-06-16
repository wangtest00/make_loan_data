
def head_token(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "0","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201","x-auth-token":'Bearer '+token }
    return head
def head_token2(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es" ,"accept-encoding": "gzip","content-length": "63","host_api": "test-action.quantx.mx","x-app-name": "LanaPlus","content-type": "application/json",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201","x-auth-token":'Bearer '+token }
    return head
def head_token_kyc(token):
    head={"user-agent": "Dart/2.12 (dart:io)","x-user-language": "es","accept-encoding": "gzip","content-length": "63","host_api": "test-api.quantx.mx","x-app-name": "LanaPlus","content-type": "multipart/form-data; boundary=--dioBoundary&Happycoding-1538342764",
        "x-app-type": "10090001","x-app-version": "116","x-app-no": "201","x-auth-token":'Bearer '+token }
    return head