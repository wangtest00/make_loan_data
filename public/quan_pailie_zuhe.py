from itertools import product
from make_loan_data.public.writeExcel import *


def quan_zuhe(fenzi_name,loop_val):
    m=[]
    for i in product(*loop_val):
        lst=list(i)
        t=[",".join(str(j) for j in lst)]
        t.append(fenzi_name[0]+"测试点")
        t.reverse()   #列表倒序
        m.append(t)
    print("分子因子全排列组合=",m)
    return m

def duqu_zuhe():
    all_list=WriteExcel().read_Excel_Xls('C:\\Users\\wangshuang\\Desktop\\demo1.xls')
    new_list=[]
    fenzi_name=[]
    for i in range(1,len(all_list)):#从第二行开始打印
        #print(all_list[i])
        fenzi_name.append(all_list[i][0])
        all_list[i].pop(0)  #删掉第一个元素
        new_list.append(all_list[i])
    #print('fenzi_name=',fenzi_name)
    fenzi_name=[",".join(str(j) for j in fenzi_name)]
    print('fenzi_name=',fenzi_name)
    zuhe=quan_zuhe(fenzi_name,new_list)
    for x in range(len(zuhe)):
        #print(zuhe[x])
        if '1.0' in zuhe[x][1]  and 'q' in zuhe[x][1] and 'z' in zuhe[x][1]:
            zuhe[x].append("预期结果【真】")
            print(zuhe[x])
        elif '2.0' in zuhe[x][1] and 'q' in zuhe[x][1] and 'z' in zuhe[x][1]:
            zuhe[x].append("预期结果【真】")
            print(zuhe[x])
        else:
            zuhe[x].append("预期结果【假】")
            print(zuhe[x])
    #WriteExcel().write_Excel_Xls(zuhe)


if __name__ == '__main__':
    duqu_zuhe()