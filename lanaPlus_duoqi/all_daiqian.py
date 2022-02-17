from concurrent.futures import ThreadPoolExecutor  # 线程池执行器
from make_loan_data.lanaPlus_duoqi.first_apply_lp_duoqi import *
import threading


def all_daiqian(x):
    auto_test()

if __name__ == '__main__':
    print("开始执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # 创建一个包含5条线程的线程池
    with ThreadPoolExecutor(max_workers=5) as pool:
        for i in range(5):
            print(threading.current_thread().name + '---' + str(i))
            res = pool.submit(all_daiqian,i)
            print("该任务执行结果=",res.result())
            print("该任务是否结束=",res.done())
        pool.shutdown()
    print("结束执行时间=",str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))