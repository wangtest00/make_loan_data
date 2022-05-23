import requests
#印度-风控定时任务【调度】
def india_thirdservice():
    r=requests.post('https://test-api-01.quantstack.in/api/third_service/excute?count=10')
    print('调风控接口响应=',r.json())

if __name__ == '__main__':
    india_thirdservice()