#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 基础包：接口测试的封装
import requests
import json

class Api_Request(object):
    def change_type(self,value):
        """
        对dict类型进行中文识别
        :param value: 传的数据值
        :return: 转码后的值
        """
        result = json.dumps(value)
        return result

    def api_Request(self,method, url, data, headers):
        """
        定义一个请求接口的方法和需要的参数
        :param method: 请求类型
        :param url: 请求地址
        :param data: 请求参数
        :param headers: 请求headers
        :return: code码
        """
        global results
        try:
            if method == ("post" or "POST"):
                results = requests.post(url, data=data, headers=headers,verify=False)
            if method == ("get" or "GET"):
                results = requests.get(url, data=data, headers=headers)
            response=self.checkApi(url,results)
            return response
        except Exception as e:
            print ("请求失败 %s" % e)
            return 0

    def checkApi(self,url,response):
        if response.status_code==200:
            t=response.json()
            print('请求接口地址=',url,'checkApi响应=',t)
            return t
        else:
            print("测试环境可能不稳定，接口返回=",url,response.content)
            return 0
if __name__ == '__main__':
    data={'appName': 'Turrant', 'appNo': '104', 'appType': '10090001', 'code': '5555', 'gaid': '12303937-ccde-46ee-a455-5146d36344dd', 'ipAddr': '192.168.20.223', 'osVersion': '10', 'phoneType': 'HUAWEI', 'registNo': '8485840000', 'utmCampaign': '', 'utmContent': '', 'utmMedium': '', 'utmSource': '', 'utmTerm': '', 'versionNo': '1.0.0'}
    print(Api_Request().change_type(data))