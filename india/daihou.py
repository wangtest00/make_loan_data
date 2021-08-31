import requests,json
from data.var_india import *
from public.check_api import *
from public.dataBase import *

@hulue_error()
def payout_mock_apply(loanNo,custNo):
    data={
    "loanNo": loanNo,
    "custNo": custNo,
    "appNo": "102"
}
    r=requests.post("https://test-pay.quantstack.in/api/fin/payout/mock/apply",data=json.dumps(data),headers=head_india_pay,verify=False)
    print("调提现mock接口，暂时忽略报错",r.json())

def chaXun_Stat(loanNo):
    sql="select before_stat from lo_loan_dtl where loan_no='"+loanNo+"';"
    before_stat=DataBase(inter_db).get_one(sql)
    if before_stat[0]=='10260005':
        print("贷前状态已变更为:【已提现】",loanNo)
    else:
        print("贷前状态未变更,查询到状态=",before_stat[0],loanNo)

if __name__ == '__main__':
    payout_mock_apply('L1022108318120871775139594240','C1022108318120871626262773760')