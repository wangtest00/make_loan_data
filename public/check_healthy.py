from common.api_Request import *
import yaml,json

class ApiTest(Api_Request):
    def __init__(self):
        self.apiTestName=Api_Request()
        self.f = open('C:\\Users\\root\\PycharmProjects\\make_loan_data\\data\\mex-host.yml', 'r', encoding='utf-8')
        self.conf = self.f.read()
        self.y = yaml.load(self.conf,Loader=yaml.FullLoader)

class Check_Healthy(ApiTest):
    def checkAllTest(self):
        x=self.y['host_test']
        self.checkHealth(x)

    def checkAllProd(self):
        x=self.y['host_prod']
        self.checkHealth(x)

    def checkHealth(self,x):
        ApiTest.api_Request(self, 'get', x['host_api'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_api2'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_api3'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_action'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_pay'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_coll'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_coll2'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_coll3'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_coll_data'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt2'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt3'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_msg'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_target'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_duanlian'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_asset'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_cms'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_timer'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_payment'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_data'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_interface'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_process'] + x['url_health'], '', '')
        ApiTest.api_Request(self, 'get', x['host_risk'] + x['url_health'], '', '')


if __name__ == '__main__':
    #Check_Healthy().checkAllProd()
    Check_Healthy().checkAllTest()