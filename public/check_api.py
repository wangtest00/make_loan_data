
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