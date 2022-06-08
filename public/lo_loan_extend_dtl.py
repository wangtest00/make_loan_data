from database.dataBase_mex import *


def cx_update_repaydate():
    sql0="select LOAN_NO,FINAL_REPAY_DATE from lo_loan_extend_dtl;"
    t0=DataBase(which_db).get_all(sql0)
    for i in range(len(t0)):
        print(t0[i])
        sql1="select t.repay_date,t.INST_NUM,t.REMARK from dc_flow_dtl t where t.LOAN_NO='"+t0[i][0]+"' and t.REMARK is not null;"
        t1=DataBase(which_db).get_all(sql1)
        print(t1)
        repaydate=t1[0][0]
        inst_num=t1[0][1]
        remark=t1[0][2]
        finam_repay_date=t0[i][1]
        print(repaydate,inst_num,remark,finam_repay_date)
        sql2="select t.repay_date from lo_loan_plan_dtl t where t.LOAN_NO='"+t0[i][0]+"' and t.INST_NUM='"+inst_num+"';"
        t2=DataBase(which_db).get_all(sql2)
        print(t2)
        sql3="select repay_date from fin_ad_detail_dtl where LOAN_NO='"+t0[i][0]+"' and REMARK='"+remark+"';"
        t3=DataBase(which_db).get_all(sql3)
        print(t3)
        sql4="select repay_date from fin_ad_dtl where LOAN_NO='"+t0[i][0]+"'  and REMARK='"+remark+"';"
        t4=DataBase(which_db).get_all(sql4)
        print(t4)
        sql5="select repay_date from fin_fee_reduce_dtl where LOAN_NO='"+t0[i][0]+"'and REMARK='"+remark+"';"
        t5=DataBase(which_db).get_all(sql5)
        print(t5)
        sql6="select repay_date from pay_tran_dtl where LOAN_NO='"+t0[i][0]+"';"
        t6=DataBase(which_db).get_all(sql6)
        print(t6)
        sql7="select repay_date from pay_tran_log where LOAN_NO='"+t0[i][0]+"';"
        t7=DataBase(which_db).get_all(sql7)
        print(t7)
        sql8="select repay_date from fin_tran_repay_dtl where LOAN_NO='"+t0[i][0]+"';"
        t8=DataBase(which_db).get_all(sql8)
        print(t8)
        sql9="select repay_date from rpt_lo_repay_plan_dtl where LOAN_NO='"+t0[i][0]+"';"
        t9=DataBase(which_db).get_all(sql9)
        print(t9)
        sql9="select repay_date from pay_closed_handle_dtl where LOAN_NO='"+t0[i][0]+"';"
        t9=DataBase(which_db).get_all(sql9)
        print(t9)
        sql10="select repay_date from fin_tob_repay_dtl where LOAN_NO='"+t0[i][0]+"';"
        t10=DataBase(which_db).get_all(sql10)
        print(t10)


def repay_date_confirm():
    table=['lo_loan_plan_dtl','dc_flow_dtl','fin_ad_dtl','fin_ad_detail_dtl','fin_fee_reduce_dtl','pay_tran_dtl','fin_tran_repay_dtl','rpt_lo_repay_plan_dtl','pay_closed_handle_dtl','fin_tob_repay_dtl']
    for table in table:
        sql='''select count(1) as diff_cnt
                          from (select a.repay_date, a.cnt - ifnull(b.cnt, 0) as diff
                                  from (select repay_date, count(1) as cnt
                                          from lo_loan_before_extend_dtl
                                         group by repay_date) a
                                  left join (select z.repay_date, count(1) as cnt
                                              from (select e.initial_repay_date as repay_date,
                                                           e.loan_no
                                                      from ''' +table+''' p
                                                     inner join lo_loan_extend_dtl e
                                                        on p.loan_no = e.loan_no
                                                       and p.repay_date = e.final_repay_date
                                                     where e.initial_repay_date =
                                                           date_format(date('20220107'), '%Y%m%d')
                                                     group by e.initial_repay_date, loan_no) z
                                             group by repay_date) b
                                    on a.repay_date = b.repay_date) t
                         where t.diff <> 0'''
        t=DataBase(which_db).get_one(sql)
        if t[0]!=0:
            print(t,table)
        else:
            pass

repay_date_confirm()