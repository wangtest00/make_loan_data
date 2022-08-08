import json,requests,random
from data.var_mex_backup import *


#注意可能会发送真实短信出去
def send_phone_code():
    header={"X-App-No": "201","X-App-Name": "LanaPlus","X-App-Version": "100","X-App-Type": "10090001","Content-Type": "application/json","User-Agent": "PostmanRuntime/7.28.0","Accept": "*/*","Postman-Token": "d4cecd3c-ef0d-497b-bb5c-83961855042c","Host": "test-api.quantx.mx","Accept-Encoding": "gzip, deflate, br","Connection": "keep-alive","Content-Length": "32"}
    #randnum=str(random.randint(1000000000,9999999999)) #10位随机数
    randnum='9383893927'
    data={"phoneNo":randnum}
    r=requests.post(host_api+"/api/cust/phone/code",data=json.dumps(data),headers=header)
    print(randnum,r.json())

def push_msg():
    appNo='201'
    header={"X-App-No": appNo,"X-App-Name": "LanaPlus","X-App-Version": "100","X-App-Type": "10090001","Content-Type": "application/json","User-Agent": "PostmanRuntime/7.28.0","Accept": "*/*","Postman-Token": "d4cecd3c-ef0d-497b-bb5c-83961855042c","Host": "test-api.quantx.mx","Accept-Encoding": "gzip, deflate, br","Connection": "keep-alive","Content-Length": "32"}
    data={
    "appNo": appNo,
    #"templateNo":"manual_check_push-La",#测试
    "templateNo":"manual_check_push-LP",#生产
    "phoneList": [
        "9383893927"
    ]
}
    r=requests.post(host_msg+'/api/interface/third/push',data=json.dumps(data),headers=header)
    print(r.json())

if __name__ == '__main__':
    for i in range(1):
        push_msg()
