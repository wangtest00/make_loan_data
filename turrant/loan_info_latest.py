import requests,json
from turrant.daiqian_104 import *


# multipart/form-data表单格式请求接口
class MultipartFormData(object):
    """multipart/form-data格式转化"""
    @staticmethod
    def format(data, boundary="----WebKitFormBoundary7MA4YWxkTrZu0gW", headers={}):
        """
        form data
        :param: data:  {"req":{"cno":"18990876","flag":"Y"},"ts":1,"sig":1,"v": 2.0}
        :param: boundary: "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        :param: headers: 包含boundary的头信息；如果boundary与headers同时存在以headers为准
        :return: str
        :rtype: str
        """
        #从headers中提取boundary信息
        if "content-type" in headers:
            fd_val = str(headers["content-type"])
            if "boundary" in fd_val:
                fd_val = fd_val.split(";")[1].strip()
                boundary = fd_val.split("=")[1].strip()
            else:
                raise "multipart/form-data头信息错误，请检查content-type key是否包含boundary"
        #form-data格式定式
        jion_str = '--{}\r\nContent-Disposition: form-data; name="{}"\r\n\r\n{}\r\n'
        end_str = "--{}--".format(boundary)
        args_str = ""
        if not isinstance(data, dict):
            raise "multipart/form-data参数错误，data参数应为dict类型"
        for key, value in data.items():
            args_str = args_str + jion_str.format(boundary, key, value)

        args_str = args_str + end_str.format(boundary)
        args_str = args_str.replace("\'", "\"")
        return args_str

def loan_info_latest(registNo,headf):
    #data={"registNo":registNo,"appNo":app_no}
    #mh = MultipartFormData().format(data=data, headers=headf)
    #print(mh)
    r=requests.get(host_api+"/api/v2/user/loan/latest/"+registNo,headers=headf)
    #print(r.json())
    t=r.json()
    loan_info_list=[]
    if t['data']['loanInfoData']['instNum'] is not None:
        instNum=str(t['data']['loanInfoData']['instNum'])
        loanAmt=str(t['data']['loanInfoData']['loanAmount'])
        loan_info_list.append(instNum)
        loan_info_list.append(loanAmt)
        print(loan_info_list)
        return loan_info_list
    else:
        print("最近一笔贷款接口获取到：贷款期数为空,不继续执行了")
        return 0

if __name__ == '__main__':
    token=login_code('9441600481')
    headt=head_token(token)
    loan_info_latest('9441600481',headt)
    print('666666666666666')