# -*- coding:utf-8 -*-
import xmind
from public.writeExcel import *


def make_case():
    # 加载已有xmind文件，如果不存在，则新建
    workbook = xmind.load('C:\\Users\\wangshuang\\Desktop\\授信产品-测试分析0817.xmind')
    t=workbook.getData()[0]
    print(t) # 获取整个xmind数据(字典的形式)
    t=t['topic']
    t=t['topics']
    #print(len(t))
    case_list=[]
    for k in range(len(t)):
        m=t[k]
        print('一级模块名称=',m['title'])
        yiji=m['title']
        m=m['topics']
        print('111111111',len(m))
        for s in range(len(m)):
            y=m[s]
            print('222222222',y)
            print('二级模块名称=',y['title'])  #打印模块名
            erji=y['title']
            y=y['topics']
            #print(len(m))    #打印主测试点个数
            for i in range(len(y)):
                #print('mokuai=',m[i]['title']) #打印主测试点名称
                sanji=y[i]['title']
                y[i]=y[i]['topics']
                for j in range(len(y[i])):
                    #print('case=',m[i][j]['title']) #打印详细测试点
                    case=y[i][j]['title']
                    case_list.append(yiji)
                    case_list.append(erji)
                    case_list.append('刘玲玲|王爽')
                    case_list.append('功能测试')
                    case_list.append('P0')
                    case_list.append('无')
                    case_list.append(sanji+case)
                    case_list.append('测试通过')
                    case_list.append('刘玲玲|王爽')
                    case_list.append('无')
                    #print(case_list)
    n=10  #每10个一组
    case_list=[case_list[i:i+n] for i in range(0,len(case_list),n)]
    print(case_list) #一维变二维
    #WriteExcel().write_Excel_Xls_Append(case_list)

if __name__ == '__main__':
    make_case()