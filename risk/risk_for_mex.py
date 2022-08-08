import requests
#墨西哥-api调风控定时任务【调度】
def mex_thirdservice():
    r=requests.post('https://test-target.quantx.mx/api/third_service/excute?count=10')
    print('调风控接口响应=',r.json())

if __name__ == '__main__':
    mex_thirdservice()