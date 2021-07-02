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
#app页面去选择stp渠道生成待还pay_tran_dtl数据，并从接口获取到所有未还账单日，取最近一期去模拟银行回调还款-单期足额
def getRepayDateList_stp(registNo,loanNo):
    #registNo='9136996496' loanNo='L2012106298098189178824597504'
    sql="select CUST_NO from cu_cust_reg_dtl where REGIST_NO='"+registNo+"';"
    custNo=DataBase(which_db).get_one(sql)
    custNo=custNo[0]
    token=login_pwd(registNo)
    headt=head_token(token)
    getRepayDate_List=getRepayDateList(registNo,headt)
    repayDate=getRepayDate_List[0]  #获取最近一期未还的账单日
    print("当前最近一期未还repayDate=",repayDate)
    repayList=repay(custNo,loanNo,repayDate,headt)
                 #还款账号       金额
    stp_repayment(repayList[1],repayList[0])  #单期足额还款
if __name__ == '__main__':
    stp_repayment('646180244001045269','2050')
    #getRepayDateList_stp('9421361124','L2012107028099174202151706624')