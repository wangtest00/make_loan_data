from lanaPlus_danqi.daiHou import *
from lanaPlus_danqi.gaiShu_mex import *
from lanaPlus_danqi.daiQian import *
from common.calculate import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#改编码方便jenkins运行
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="gb18030")
daiQian=DaiQian_Danqi()
#复客再次申请贷款，接口正案例
def reApply():
    custNo=get_CustNO()
    #custNo='C2012201098168704182996631552'
    sql="select REGIST_NO from cu_cust_reg_dtl where CUST_NO='"+custNo+"';"
    registNo=DataBase(configs).get_one(sql)
    registNo=registNo[0]
    code = compute_code(registNo)
    token = daiQian.login_code(registNo, code)
    headt = head_token(token)
    #在app申请贷款
    loanNo=daiQian.apply_loan(custNo,headt)
   # 分案
    DataBase(configs).call_4_proc()
    #审批
    approve(loanNo)
    #插入风险数据，完成匹配产品
    MockData().insert_risk(loanNo)
    #app去待提现页面申请贷款
    daiQian.withdraw(registNo,custNo,loanNo,headt)
    #贷前状态变更为“待提现”后的后续改数操作，模拟到提现成功
    #MockData().gaishu(loanNo)
#查询只借过一笔款且已结清的客户号
def get_CustNO():
    sql='''select  b.cust_no,count(1) as loan_cnt from
(select  a.cust_no from
lo_loan_dtl a
WHERE
	a.BEFORE_STAT = '10260005'
AND a.AFTER_STAT = '10270005'
and date(a.INST_TIME)<date(now())
GROUP BY a.cust_no
HAVING count(1) =1
)a INNER JOIN lo_loan_dtl b on a.cust_no=b.cust_no inner join cu_cust_reg_dtl c on b.cust_no=c.cust_no left join cu_cust_bank_card_dtl d on c.CUST_NO=d.CUST_NO
where c.APP_NO="'''+appNo+'''" and d.USEABLE='10000001' and d.BANK_ACCT_NO is not null
group by  b.cust_no
HAVING loan_cnt=1 order by b.INST_TIME desc;'''
    custNo=DataBase(configs).get_one(sql)
    print(sql)
    return custNo[0]
if __name__ == '__main__':
    reApply()
   # get_CustNO()