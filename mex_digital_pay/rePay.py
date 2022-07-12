import random,requests
from database.dataBase_mex import *
from mex_digital_pay.var_digital_pay import *

class RePay():
	# 模拟还款回调信息给支付平台，进件来做清结算
	def web_hook_repay_stp(self, loanNo, monto):
		sql1 = "select ASSIGN_ACCOUNT_NO from cu_cust_repayment_account where CUST_NO in (select CUST_NO from lo_loan_dtl where LOAN_NO='" + loanNo + "');"
		res = DataBase(configs).get_one(sql1)
		res = res[0]
		payment_id = str(random.randint(100000000, 999999999))
		data = {"abono": {
			"id": payment_id,
			"fechaOperacion": "20210108",
			"institucionOrdenante": "40012",
			"institucionBeneficiaria": "90646",
			"claveRastreo": "MBAN01002101080089875109",
			"monto": str(monto),
			"nombreOrdenante": "HAZEL VIRIDIANA RUIZ RICO",
			"tipoCuentaOrdenante": "40",
			"cuentaOrdenante": "012420028362208190",
			"rfcCurpOrdenante": "RURH8407075F8",
			"nombreBeneficiario": "STP",
			"tipoCuentaBeneficiario": "40",
			"cuentaBeneficiario": res,
			"rfcCurpBeneficiario": "null",
			"conceptoPago": "ESTELA SOLICITO TRANSFERENCIA",
			"referenciaNumerica": "701210",
			"empresa": "QUANTX_TECH"
		}
		}
		r = requests.post(host_dig_pay+'/api/web_hook/repay/stp', data=json.dumps(data),headers=head_dig_pay, verify=False)
		print(r.json())

if __name__ == '__main__':
	RePay().web_hook_repay_stp('L2012207128235115601509679104','1')