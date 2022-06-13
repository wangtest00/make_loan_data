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
        ApiTest.api_Request(self, 'get', x['host_api'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_action'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_pay'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_coll'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_coll2'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_coll3'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_coll_data'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt2'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_mgt3'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_msg'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_target'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_duanlian'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_asset'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_cms'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_timer'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_payment'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_data'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_interface'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_process'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_risk'] + '/api/ext/health', '', '')

    def checkAllProd(self):
        x=self.y['host_prod']
        ApiTest.api_Request(self, 'get', x['host_api'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_api2'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_api3'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_action'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_pay'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_coll'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_coll2'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_coll3'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_coll_data'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_mgt'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_mgt2'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_mgt3'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_msg'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_target'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_duanlian'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_asset'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_cms'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_timer'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_payment'] + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', x['host_risk_data'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_risk_interface'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_risk_process'] + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', x['host_risk'] + '/api/ext/health','','')



if __name__ == '__main__':
    Check_Healthy().checkAllProd()
   # Check_Healthy().checkAllTest()