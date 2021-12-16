import string,requests,json,datetime
from make_loan_data.public.dataBase import *
from make_loan_data.FeriaRapida.gaishu import *
from make_loan_data.data.var_mex import *
from make_loan_data.FeriaRapida.mex_mgt_fr import *
from make_loan_data.FeriaRapida.heads import *
from make_loan_data.public.check_api import *
from make_loan_data.FeriaRapida.daihou import *
import io,sys
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

#复客再次申请贷款，接口正案例
def reApply():
    custNo=get_CustNO()
    sql="select REGIST_NO from cu_cust_reg_dtl where CUST_NO='"+custNo+"';"
    registNo=DataBase(which_db).get_one(sql)
    registNo=registNo[0]
    print(registNo)
    update_pwd(registNo)
    token=login_pwd(registNo)
    headt=head_token(token)
    #在app申请贷款
    loanNo=apply_loan(custNo,headt)
    #分案
    DataBase('mex_pdl_loan').call_4_proc()
    #审批
    approve(loanNo)
    #插入风险数据，完成匹配产品
    insert_risk(loanNo)
    #app去待提现页面申请贷款
    withdraw(registNo,custNo,loanNo,headt)
    #贷前状态变更为“待提现”后的后续改数操作，模拟到提现成功
    gaishu(loanNo)
#查询只借过一笔款且已结清的客户号
def get_CustNO():
    sql='''select  b.cust_no,count(1) as loan_cnt from
(select  a.cust_no from
lo_loan_dtl a
WHERE
	a.BEFORE_STAT = '10260005'
AND a.AFTER_STAT = '10270005'
GROUP BY a.cust_no
HAVING count(1) =1
)a INNER JOIN lo_loan_dtl b on a.cust_no=b.cust_no inner join cu_cust_reg_dtl c on b.cust_no=c.cust_no where c.APP_NO="'''+appNo+'''"
group by  b.cust_no
HAVING loan_cnt=1;'''
    custNo=DataBase(which_db).get_one(sql)
    print(custNo[0])
    return custNo[0]
if __name__ == '__main__':
    reApply()
    get_CustNO()