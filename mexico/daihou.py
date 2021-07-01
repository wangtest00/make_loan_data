import requests,json
import random
from data.var_mex import *
from mexico.daiqian_lanaplus import *
from public.dataBase import *

#模拟银行回调接口-模拟还款stp（只需修改卡号cuentaBeneficiario和金额monto）
def stp_repayment(cuentaBeneficiario,monto):
    data={"abono":{"id":"37755992","fechaOperacion":"20210108","institucionOrdenante":"40012","institucionBeneficiaria":"90646","claveRastreo":"MBAN01002101080089875109","monto":monto,
                   "nombreOrdenante":"HAZEL VIRIDIANA RUIZ RICO               ","tipoCuentaOrdenante":"40","cuentaOrdenante":"012420028362208190","rfcCurpOrdenante":"RURH8407075F8","nombreBeneficiario":"STP                                     ",
                   "tipoCuentaBeneficiario":"40","cuentaBeneficiario":cuentaBeneficiario,"rfcCurpBeneficiario":"null","conceptoPago":"ESTELA SOLICITO TRANSFERENCIA","referenciaNumerica":"701210","empresa":"QUANTX_TECH"}}
    r=requests.post(host_pay+"api/trade/stp_repayment/annon/event/webhook",data=json.dumps(data),headers=head_pay,verify=False)
    print(r.json())
    print("模拟银行回调成功")

if __name__ == '__main__':
    stp_repayment('646180244001043300','1649.70')