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
    r=requests.post(host_pay+"/api/trade/stp_repayment/annon/event/webhook",data=json.dumps(data),headers=head_pay,verify=False)
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

def oxxo_repay(amount,loanNo):
    '''
    #前提条件：用户在app页面选择OXXO渠道后调用了还款申请接口
    #注意：1.交易流水号和卡号每次生成的都不一样，可以非足额，足额，超额回调，超出金额部分科目号99
           2.返回响应结果不是errCode=1，具体还款结果可查：回款查询，pay_tran_dtl和fin_tran_repay_dtl表'''
    #查询预计交易金额，交易流水号，入账账号，条件：OXXO渠道+实际交易金额为空
    sql="select SHD_TRAN_AMT,tran_order_no,in_acct_no from pay_tran_dtl t where LOAN_NO='"+loanNo+"' and TRAN_CHAN_NAME ='Conekta支付渠道' and ACT_TRAN_AMT is null;"
    three_list=DataBase(which_db).get_one(sql)
    print(three_list)
    data={"data": {"object": {
			"livemode": False,
			"amount": int(amount)*100,
			"currency": "",
			"payment_status": "paid",
			"amount_refunded": 0,
			"customer_info": {"email": "","phone": "","name": "","object": ""},"object": "",
			"id": three_list[1],
			"metadata": {},
			"created_at": 0,
			"updated_at": 0,
			"line_items": {
				"object": "",
				"has_more": False,
				"total": 0,
				"data": [
					{"name": "",
						"unit_price": 0,
						"quantity": 0,
						"object": "",
						"id": "",
						"parent_id": "",
						"metadata": {},
						"antifraud_info": {}
					}
				]
			},
			"charges": {"object": "",
				"has_more": False,
				"total": 0,
				"data": [
					{
						"id": "",
						"livemode": False,
						"created_at": 0,
						"currency": "",
						"payment_method": {
							"service_name": "OxxoPay",
							"barcode_url": "https://s3.amazonaws.com/cash_payment_barcodes/84000964785462.png",
							"object": "",
							"type": "",
							"expires_at": 0,
							"store_name": "OXXO",
							"reference": three_list[2]
						},
						"object": "",
						"description": "",
						"status": "",
						"amount": 0,
						"paid_at": 0,
						"fee": 0,
						"customer_id": "",
						"order_id": ""
					}
				]
			}
		},
		"previous_attributes": {}
	},
	"livemode": False,
	"webhook_status": "",
	"id": "",
	"object": "",
	"type": "order.paid",
	"created_at": 0,
	"webhook_logs": [
		{
			"id": "",
			"url": "",
			"failed_attempts": 0,
			"last_http_response_status": 0,
			"object": "",
			"last_attempted_at": 0
		}
	]
}

    r=requests.post(host_pay+"/api/trade/conekta/annon/event/webhook",data=json.dumps(data),verify=False)
    print(r.json())

if __name__ == '__main__':
    stp_repayment('646180244001045337','1200')
   # getRepayDateList_stp('8545945423','L2012106248096585023351070720')
    #oxxo_repay('120','L2012107058100314170245292032')