from data.var_mex_credit import *
import requests,json,time


#数据上传
def upload():
    r=requests.post(host_mgt+"/api/insecure/collection/upload/new",verify=False)
    print(r.json())
#数据同步
def sync():
    r=requests.post(host_coll+'/api/insecure/task/collection/data/sync',verify=False)
    print(r.json())


def jin_cuishou():
    upload()
    time.sleep(3)
    sync()

if __name__ == '__main__':
    jin_cuishou()