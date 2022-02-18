import json,requests,random
from make_loan_data.data.var_mex_lp_duoqi import *
#注意可能会发送真实短信出去

def check_api(r):
    try:
        if r.status_code==200:
            t=r.json()
            if t['errorCode']==0:
                print("校验成功，接口返回=",t)
                return t
            else:
                print("校验失败，接口返回=",t)
                return 0
        else:
            print("环境可能不稳定，接口返回=",r.content)
            return 0
    except Exception as e:
        print("捕获到异常：",e)
        return 0
def send_phone_code():
    header={"X-App-No": "201","X-App-Name": "LanaPlus","X-App-Version": "100","X-App-Type": "10090001","Content-Type": "application/json","User-Agent": "PostmanRuntime/7.28.0","Accept": "*/*","Postman-Token": "d4cecd3c-ef0d-497b-bb5c-83961855042c","Host": "test-api.quantx.mx","Accept-Encoding": "gzip, deflate, br","Connection": "keep-alive","Content-Length": "32"}
    randnum=str(random.randint(1000000000,9999999999)) #10位随机数
    data={"phoneNo":randnum}
    r=requests.post(host_api+"/api/cust/phone/code",data=json.dumps(data),headers=header)
    print(randnum)
    check_api(r)


if __name__ == '__main__':
    for i in range(500):
        send_phone_code()
