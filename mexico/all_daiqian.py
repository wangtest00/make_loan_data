from concurrent.futures import ThreadPoolExecutor  # 线程池执行器
from mexico.first_apply import *

def all_daiqian(x):
    auto_test()

if __name__ == '__main__':
    print("开始执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i in range(2):
            res = pool.submit(all_daiqian,i)
    print("结束执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))