import string,requests,json,datetime
from public.dataBase import *
from mexico.gaishu import *
from data.var_mex import *
from mexico.mex_mgt import *
from mexico.heads import *
from public.check_api import *
from mexico.daihou import *
import io,sys
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")

#复客再次申请贷款，接口正案例
def reApply():
    custNo=getCustNO()
    sql="select REGIST_NO from cu_cust_reg_dtl where CUST_NO='"+custNo+"';"
    registNo=DataBase(which_db).get_one(sql)
    registNo=registNo[0]
    # registNo='9444765324'
    # custNo='C2012107088101421827813318656'
    print(registNo)
    update_pwd(registNo)
    # token=login_pwd(registNo)
    # headt=head_token(token)
    # #在app申请贷款
    # loanNo=apply_loan(custNo,headt)
    # #分案
    # DataBase('mex_pdl_loan').call_4_proc()
    # #审批
    # pl_shenpi()
    # #插入风险数据，完成匹配产品
    # insert_risk(loanNo)
    # #app去待提现页面申请贷款
    # withdraw(registNo,custNo,loanNo,headt)
    # #贷前状态变更为“待提现”后的后续改数操作，模拟到提现成功
    # gaishu(loanNo)
#查询只借过一笔款且已结清的客户号
def getCustNO():
    sql='''select  b.cust_no,count(1) as loan_cnt from
(select  a.cust_no from
lo_loan_dtl a
WHERE
	a.BEFORE_STAT = '10260005'
AND a.AFTER_STAT = '10270005'
GROUP BY a.cust_no
HAVING count(1) =1
)a INNER JOIN lo_loan_dtl b on a.cust_no=b.cust_no
group by  b.cust_no
HAVING loan_cnt=1;'''
    custNo=DataBase(which_db).get_one(sql)
    print(custNo[0])
    return custNo[0]
if __name__ == '__main__':
    reApply()
    #getCustNO()