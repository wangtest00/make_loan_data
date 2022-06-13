from concurrent.futures import ThreadPoolExecutor  # 线程池执行器
from cashTm.daiQian import *
import threading,datetime,time


def all_daiqian():
    daiQian = DaiQian_CashTm()
    registNo = '8989850000'  # 10位随机数
    token = daiQian.login_code(registNo)
    headt = daiQian.head_token(token)
    for i in range(2):
        custNo = daiQian.cert_auth(registNo, headt)

if __name__ == '__main__':
    try:
        i = 0
        # 开启线程数目
        tasks_number = 200000
        print('测试启动')
        #time1 = time.clock()
        while i < tasks_number:
            t = threading.Thread(target=all_daiqian)
            t.start()
            i += 1
        # time2 = time.clock()
        # times = time2 - time1
        # print(times / tasks_number)
    except Exception as e:
        print(e)