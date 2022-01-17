import random
from make_loan_data.lanaPlus_duoqi.daiqian_lanaplus import *
from make_loan_data.public.dataBase import *
from make_loan_data.data.var_mex_lp import *


#datet=str(time.time()*1000000)[:-2]   #16位时间戳
#用户在app操作了添加绑卡信息，同意协议并点击确认提现按钮，贷前状态变更为“待提现”后的后续改数操作，模拟到提现成功
def gaishu(loan_no):
    randnum=str(random.randint(10000000,99999999)) #8位随机数
    sql1="update fin_tran_pay_dtl set tran_pay_stat='10420001' where loan_no='"+loan_no+"';"
    sql2="select tran_flow_no from pay_tran_dtl where LOAN_NO='"+loan_no+"';"
    DataBase(which_db).executeUpdateSql(sql1)
    time.sleep(1)
    DataBase(which_db).executeUpdateSql(sql1)
    time.sleep(1)
    tran_flow_no=DataBase(which_db).get_one(sql2)
    sql3="update pay_tran_dtl set utr_no='"+tran_flow_no[0]+"' ,TRAN_STAT='10220001',tran_order_no='"+randnum+"' where  LOAN_NO='"+loan_no+"';"
    DataBase(which_db).executeUpdateSql(sql3)
    time.sleep(1)
    sql4="update lo_loan_dtl set before_stat='10260008' where loan_no='"+loan_no+"';"
    DataBase(which_db).executeUpdateSql(sql4)
    time.sleep(1)
    stp_payout(loan_no,tran_flow_no[0],randnum,'0000')   #模拟回调提现成功
    tran_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    sql5="update fin_tran_pay_dtl set tran_pay_stat='10420002',tran_time='"+tran_time+"' where loan_no='"+loan_no+"';"
    DataBase(which_db).executeUpdateSql(sql5)
    sql6="DELETE from pay_payout_retry where loan_no='"+loan_no+"';" # 需要删除，否则调重试申请会置为提现失败
    DataBase(which_db).executeUpdateSql(sql6)

#墨西哥-提现mock    # date=int(str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')) #日期时分秒
def stp_payout(loan_no,folioOrigen,id,code):
    data={"causaDevolucion": { "code": 16,"msg": "Tipo de operación errónea"},"empresa": "ASSERTIVE","estado":
                             { "code": code, "msg": "canll"},"folioOrigen": folioOrigen,"id":int(id)}
    print(data)
    r=requests.post("https://test-pay.quantx.mx/api/trade/stp_payout/annon/event/webhook",data=json.dumps(data),headers=head_pay,verify=False)
    t=r.json()
    print(t)
    if t['errorCode']==0:
        print("执行墨西哥模拟提现接口成功",loan_no)
    else:
        print("执行墨西哥模拟提现接口失败",loan_no)
    sql="select before_stat from lo_loan_dtl where loan_no='"+loan_no+"';"
    before_stat=DataBase(which_db).get_one(sql)
    if before_stat[0]=='10260005':
        print("贷前状态已变更为:【已提现】",loan_no)
    else:
        print("贷前状态未变更,查询到状态=",before_stat[0])

#5.借据贷前状态=“待匹配产品”，贷款与客户基本关系表' 需要手动插数risk_level AA和risk_score 20120701(印度)，25002400或26002401（墨西哥）（调度系统跑批识别出来，分配对应产品）
def insert_risk(loan_no):
    sql="update lo_loan_cust_rel set risk_level='U_NewA',risk_score='"+prodNo+"' where LOAN_NO='"+loan_no+"';"
    DataBase(which_db).executeUpdateSql(sql)
    DataBase(which_db).call_many_proc()

if __name__ == '__main__':
    gaishu('L2012201118169476721079418880')
    #stp_payout('L2012112238162296529248518144','w2021122303562166300100560040','31564088')
    #insert_risk('L2012201118169476721079418880')