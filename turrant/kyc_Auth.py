# multipart/form-data
import requests
from turrant.daiQian import *

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

headers = {
        'content-type': "multipart/form-data; boundary=89795e05-6272-4b47-a620-b40b5a0ebcdc",
        'cache-control': "no-cache",
    }
data = {
    "custNo":"C1022201258174182555088781312",
    "kycType":"10070015",
    "fileSource":'10080001',
    "kycImg":1,
    }

#mh = MultipartFormData.format(data=data, headers=headers)
#print(mh)


def kyc_auth(custNo,headt):
    files={'kycImg':('zheng_main.jpg',open(r'D:\pic\zheng_main.jpg', 'rb'),'image/jpeg'),'custNo':(None,custNo),'kycType':(None,'10070015'),'fileSource':(None,'10080001') }
    r=requests.post("https://test-appa.quantstack.in/api/cust_india/kyc/auth?lang=en",files=files,headers=headt,verify=False)
    print(r.json())

registNo='8383834444'
token=login_code(registNo)
headt=head_token_f(token)
kyc_auth('C1022201258174182555088781312',headt)