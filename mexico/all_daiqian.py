from concurrent.futures import ThreadPoolExecutor  # 线程池执行器
from mexico.first_apply import *
import threading
from public.check_api import *


def all_daiqian(x):
    auto_test()

if __name__ == '__main__':
    print("开始执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # 创建一个包含2条线程的线程池
    with ThreadPoolExecutor(max_workers=5) as pool:
        for i in range(2):
            print(threading.current_thread().name + '---' + str(i))
            res = pool.submit(all_daiqian,i)
            print("该任务执行结果=",res.result())
            print("该任务是否结束=",res.done())
        pool.shutdown()
    print("结束执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))