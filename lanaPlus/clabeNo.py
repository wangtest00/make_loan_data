from make_loan_data.public.dataBase import *

quanzhi=[]
for j in range(6):
    for i in range(3,13,4):
        quanzhi.append(i%10)
        #print(i%10)
#print(quanzhi[:-1])
quanzhi_list=quanzhi[:-1]  #权重因子
def jiaoyan_clabeNo(clabeNo):
    if len(clabeNo)==18:
        sum_quanzhi=0
        for x in range(17):
            #print(quanzhi_list[x],"*",clabeNo[x])
            sum_quanzhi=sum_quanzhi+(int(quanzhi_list[x])*int(clabeNo[x]))%10
        #print('sum_quanzhi=',sum_quanzhi)
        #print(sum_quanzhi%10)
        jiaoyanwei=10-sum_quanzhi%10
        jiaoyanwei=jiaoyanwei%10
        #print('jiaoyanwei取模后=',jiaoyanwei%10)
        if clabeNo[:17]+str(jiaoyanwei)==clabeNo:
            #print("clabeNo有效")
            return 0
        else:
            print("clabeNo无效:",clabeNo)
            return clabeNo
    else:
        #print("卡号不足18位，一律处理为失效")
        return clabeNo

def cx_clableNo():
    sql='''select BANK_ACCT_NO from cu_cust_bank_card_dtl;
    '''
    clableNo=DataBase(which_db).get_all(sql)
    print(len(clableNo),clableNo)
    m=[]
    for i in range(len(clableNo)):
        #print(clableNo[i][0])
        if jiaoyan_clabeNo(clableNo[i][0])==0:
            pass
        else:
            m.append(jiaoyan_clabeNo(clableNo[i][0]))
    print(len(m),m)
    sql2='''  #查询处理为失效的银行卡号
    select BANK_ACCT_NO from cu_cust_bank_card_dtl where USEABLE='10000000' and REMARK='批量处理不符合校验规则银行卡为失效状态';
'''
    chengxu_clableNo=DataBase(which_db).get_all(sql2)
    #print(len(chengxu_clableNo),chengxu_clableNo)
    n=[]
    for j in range(len(chengxu_clableNo)):
        n.append(chengxu_clableNo[j][0])
    print(len(n),n)
    for x in range(len(n)):
        if n[x] not in m:
            print(n[x])
        else:
            pass
if __name__ == '__main__':
    #cx_clableNo()
    jiaoyan_clabeNo('127180016851886127')