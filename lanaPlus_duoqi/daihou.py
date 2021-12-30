import requests,json
import random
from make_loan_data.data.var_mex_lp import *
from make_loan_data.lanaPlus_duoqi.daiqian_lanaplus import *
from make_loan_data.public.dataBase import *

#模拟银行回调接口-模拟还款stp（只需修改卡号cuentaBeneficiario和金额monto）
#1.遇到脏数据，可能会报“参数为空”
def stp_repayment(cuentaBeneficiario,monto):
	payment_id=str(random.randint(100000000,999999999))
	print("payment_id=",payment_id)
	data={"abono":{"id":payment_id,"fechaOperacion":"20210108","institucionOrdenante":"40012","institucionBeneficiaria":"90646","claveRastreo":"MBAN01002101080089875109","monto":monto,"nombreOrdenante":"HAZEL VIRIDIANA RUIZ RICO               ","tipoCuentaOrdenante":"40","cuentaOrdenante":"012420028362208190","rfcCurpOrdenante":"RURH8407075F8","nombreBeneficiario":"STP                                     ","tipoCuentaBeneficiario":"40","cuentaBeneficiario":cuentaBeneficiario,"rfcCurpBeneficiario":"null","conceptoPago":"ESTELA SOLICITO TRANSFERENCIA","referenciaNumerica":"701210","empresa":"QUANTX_TECH"}}
	#print(data)
	r=requests.post(host_pay+"/api/trade/stp_repayment/annon/event/webhook",data=json.dumps(data),headers=head_pay,verify=False)
	print(r.json())
	print("模拟银行回调成功")
#app页面去选择stp渠道生成待还pay_tran_dtl数据，并从接口获取到所有未还账单日，取最近一期去模拟银行回调还款-单期足额
def getRepayDateList_stp(registNo,loanNo,headt):
	sql="select CUST_NO from cu_cust_reg_dtl where REGIST_NO='"+registNo+"';"
	custNo=DataBase(which_db).get_one(sql)
	custNo=custNo[0]
	getRepayDate_List=getRepayDateList(registNo,headt)
	repayDate=getRepayDate_List[0]  #获取最近一期未还的账单日
	print("当前最近一期未还repayDate=",repayDate)
	repayList=repay(custNo,loanNo,repayDate,headt)
				 #还款账号       金额
	stp_repayment(repayList[1],repayList[0])  #单期足额还款STP
	stat=cx_beforeStat_afterStat(loanNo)
	if stat==('10260005','10270005'):
		print("贷后状态已结清",loanNo,stat)
	else:
		print("贷后状态未结清",loanNo,stat)


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
					}]},
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
	#stp_repayment('646180244001063717','66')
	#getRepayDateList_stp('8639812802','L2012112168159706926905753600')
	oxxo_repay('123','L2022112308164794177532657664')
	# token=login_pwd('8684947326')
	# headt=head_token(token)
	# getRepayDateList_stp('8684947326','L2012112178160096181670838272',headt)