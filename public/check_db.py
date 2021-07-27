from public.dataBase import *
import datetime

#检查放款成功，贷后状态为“正常”的贷款数据
def check_db_zc(loan_no):
    sql1="select PROD_NO,STEP_SIZE from lo_loan_prod_rel where LOAN_NO='"+loan_no+"';"  #贷款与产品关系表,查询该笔贷款产品号
    prodno=DataBase(which_db).get_one(sql1)
    print(prodno)
    sql2="select SUBJ_NO from pro_prod_fee_rel where PROD_NO='"+prodno[0]+"' and BEF_ABLE='10000000';"#查询后置收费科目号
    subj_no=DataBase(which_db).get_all(sql2)
    dict3={}
    for i in range(len(subj_no)):  #产品与费用项关系表
        sql3="select VAL from pro_prod_fee_rel where PROD_NO='"+prodno[0]+"' and BEF_ABLE='10000000' and SUBJ_NO='"+subj_no[i][0]+"';"  #查询每个科目值
        val=DataBase(which_db).get_one(sql3)
        if subj_no[i][0]=='10':
            dict3["benjin"]=val[0]
        elif subj_no[i][0]=='12':
            dict3["lixi"]=val[0]
        else:  #暂时只考虑一个渠道费
            dict3['qudaofei']=val[0]
    print(dict3)
    sql4="select APPR_AMT,LOAN_AMT,REPAY_DATE,BEFORE_STAT,AFTER_STAT,INST_TIME from lo_loan_dtl where loan_no='"+loan_no+"';"#查询基本贷款关系表
    list4=DataBase(which_db).get_one(sql4)
    print(list4)
    check(list4[0],list4[1])
    check(str(list4[0])[:-3],dict3['benjin'])
    check(list4[3],'10260005')
    check(list4[4],'10270002')
    print(type(list4[5]),str(list4[5]))
    repay_date=list4[5]+datetime.timedelta(days=int(prodno[1]))   #放款日+步长3天=账单日
    repay_date=str(repay_date)[:4]+str(repay_date)[5:7]+str(repay_date)[8:10]
    check(repay_date,list4[2])
    sql5="select TRAN_AMT,TRAN_PAY_STAT from fin_tran_pay_dtl where LOAN_NO='"+loan_no+"';"#fin_渠道放款明细表
    list5=DataBase(which_db).get_one(sql5)
    print(list5)
    sql6="select sum(val) from pro_prod_fee_rel where PROD_NO='"+prodno[0]+"'and BEF_ABLE='10000001';"#查询前置收费科目号的科目值
    s6=DataBase(which_db).get_one(sql6)
    print(type(s6[0]),s6[0])
    amt=float(dict3['benjin'])-s6[0]
    check(list5[0],amt)
    check(list5[1],'10420002')
    sql7="select * from fin_tran_repay_dtl where LOAN_NO='"+loan_no+"';"  #渠道还款明细表应该为空
    s7=DataBase(which_db).get_one(sql7)
    check(s7,None)
    sql8="select sum(TRAN_AMT) from dc_flow_dtl where LOAN_NO='"+loan_no+"' and DC_DIRECT='C';"  #借贷流水表
    sql9="select sum(TRAN_AMT) from dc_flow_dtl where LOAN_NO='"+loan_no+"' and DC_DIRECT='D';"
    s8=DataBase(which_db).get_one(sql8)
    s9=DataBase(which_db).get_one(sql9)
    trans=s8[0]-s9[0]  #交易金额=贷款金额-前置收费
    print(trans)
    sql10="select repay_date,repay_stat from lo_loan_plan_dtl  where LOAN_NO='"+loan_no+"';"#还款计划表还款日，还款状态
    loan_plan=DataBase(which_db).get_one(sql10)
    check(loan_plan[0],repay_date)
    check(loan_plan[1],'10270002')
    sql11="select REPAY_DATE,RECEIVE_AMT, AD_STAT,AD_TYPE,TRANSTER_TYPE from fin_ad_dtl where LOAN_NO='"+loan_no+"';" #应收表
    s11=DataBase(which_db).get_one(sql11)
    print(list(s11))
    yuqi_yingshou=list_append(list4[2],trans,'10360001','10370001','10440002')
    print(yuqi_yingshou)
    check_list(list(s11),yuqi_yingshou)
    sql12="select * from fin_ad_dtl_bk where LOAN_NO='"+loan_no+"';"#应收备份表为空
    s12=DataBase(which_db).get_one(sql12)
    check(s7,None)
def check(str1,str2):
    if str1==str2:
        print(str1,str2,"一致")
    else:
        print(str1,str2,"不一致")

def check_list(list1,list2):
    if list1==list2:
        print(list1,list2,"2个列表数据相同")
    else:
        print(list1,list2,"2个列表数据不相同")
def list_append(a,*args):
    list=[]
    list.append(a)
    for args in args:
        list.append(args)
    return list


if __name__ == '__main__':
    check_db_zc('L2012107218106135169306107904')
