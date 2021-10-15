import functools,traceback,time

def check_api(r):
    try:
        if r.status_code==200:
            t=r.json()
            if t['errorCode']==0:
                print("校验正确，接口返回=",t)
                return t
            else:
                print("校验错误，接口返回=",t)
                return 0
        else:
            print("环境可能不稳定，接口返回=",r.content)
            return 0
    except Exception as e:
        print("捕获到异常：",e)
        return 0

#报错后重试2次,且不会停止代码运行
def hulue_error(**outer_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            for i in range(1):
                try:
                    time.sleep(1)
                    return func(*args,**kwargs)
                except Exception as e:
                    extra={
                        'extra_method':func.__name__,
                        'extra_module':func.__module__
                    }
                    error_msg_obj={
                        'exc_info':True,
                        'extra':extra
                    }
                    #traceback.format_exc()表示哪行代码的错误
                    print('ERROR:traceback:{1}',format(traceback.format_exc()))
        return wrapper
    return decorator
