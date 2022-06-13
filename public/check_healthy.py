from common.api_Request import *
from data.var_mex_lp_duoqi import *

class ApiTest(Api_Request):
    def __init__(self):
        self.apiTestName=Api_Request()

class Check_Healthy(ApiTest):
    def checkAll(self):
        ApiTest.api_Request(self, 'get', host_api + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_action + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_pay + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_coll + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_coll_data + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_mgt + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_msg + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_target + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_duanlian + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_asset + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_cms + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_timer + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', host_payment + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', host_nx + '/api/ext/health', '', '')
        ApiTest.api_Request(self, 'get', host_risk_data + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_risk_interface + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_risk_process + '/api/ext/health','','')
        ApiTest.api_Request(self, 'get', host_risk + '/api/ext/health','','')



if __name__ == '__main__':
    Check_Healthy().checkAll()