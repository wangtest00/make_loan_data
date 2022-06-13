from lanaPlus_duoqi.daiQian import *
import random,datetime
from database.dataBase_mex import *
from data.var_mex_lp_duoqi import *

randnum=str(random.randint(10000000,99999999)) #8位随机数
class MockData():
    #用户在app操作了添加绑卡信息，同意协议并点击确认提现按钮，贷前状态变更为“待提现”后的后续改数操作，模拟到提现成功
    def gaishu(self,loanNo):
        sql1="update fin_tran_pay_dtl set tran_pay_stat='10420001' where loan_no='"+loanNo+"';"
        sql2="select tran_flow_no from pay_tran_dtl  where LOAN_NO='"+loanNo+"';"
        sql5="update lo_loan_dtl set before_stat='10260008' where loan_no='"+loanNo+"';"
        DataBase(configs).executeUpdateSql(sql1)
        DataBase(configs).executeUpdateSql(sql1)
        tran_flow_no=DataBase(configs).get_one(sql2)
        sql3="update pay_tran_dtl set utr_no='"+tran_flow_no[0]+"' ,TRAN_STAT='10220001',tran_order_no='"+randnum+"' where  LOAN_NO='"+loanNo+"';"
        DataBase(configs).executeUpdateSql(sql5)
        DataBase(configs).executeUpdateSql(sql3)
        time.sleep(1)
        self.stp_payout(loanNo,tran_flow_no[0])
        tran_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        sql6="update fin_tran_pay_dtl set tran_pay_stat='10420002',tran_time='"+tran_time+"' where loan_no='"+loanNo+"';" #解决-引导去googlePlay评分页面
        sql7="DELETE from pay_payout_retry where loan_no='"+loanNo+"';" # 需要删除，否则调重试申请会置为提现失败-回滚数据
        #DataBase(which_db).executeUpdateSql(sql6)
        DataBase(configs).executeUpdateSql(sql7)
    #墨西哥-提现mock    # date=int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) #日期时分秒
    def stp_payout(self,loanNo,folioOrigen):
        data={"causaDevolucion": { "code": 16,"msg": "Tipo de operación errónea"},"empresa": "ASSERTIVE","estado": { "code": "0000", "msg": "canll"},"folioOrigen": folioOrigen,"id":int(randnum)}
        r=requests.post(host_pay+payoutWebhookUrl,data=json.dumps(data),headers=head_pay,verify=False)
        t=r.json()
        if t['errorCode']==0:
            print("执行墨西哥模拟提现接口成功",loanNo,t)
        else:
            print("执行墨西哥模拟提现接口失败",loanNo)
        sql="select before_stat from lo_loan_dtl where loan_no='"+loanNo+"';"
        before_stat=DataBase(configs).get_one(sql)
        if before_stat[0]=='10260005':
            print("贷前状态已变更为:【已提现】",loanNo)
        else:
            print("贷前状态未变更,查询到状态=",before_stat[0])
    #5.借据贷前状态=“待匹配产品”，贷款与客户基本关系表' 需要手动插数risk_level AA和risk_score 20120701(印度)，25002400或26002401（墨西哥）（调度系统跑批识别出来，分配对应产品）
    def insert_risk(self,loanNo):
        sql="update lo_loan_cust_rel set risk_level='AA',risk_score='"+prodNo+"' where LOAN_NO='"+loanNo+"';"
        DataBase(configs).executeUpdateSql(sql)
        DataBase(configs).call_many_proc()

if __name__ == '__main__':
    MockData().gaishu('L2012205068210858853538136064')
    #stp_payout('L2012110188138307996821422080','w2021101800143309100100360099')
    #insert_risk('L2022109268130350832635019264')