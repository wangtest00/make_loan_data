import requests,json
from make_loan_data.data.var_mex import *
#催收接口
#数据上传
def upload():
    r=requests.post(host_mgt+"/api/insecure/collection/upload/new")
    print(r.json())
#数据同步
def sync():
    r=requests.post(host_coll+'/api/insecure/task/collection/data/sync')
    print(r.json())
#数据回收
def recycle():
    r=requests.post(host_coll+'/api/insecure/task/data/recycle')
    print(r.json())
#线索分配,调用该接口后，（已开启分配回收配置）会自动执行proc_ovdu_allocation_record存储过程，写数进mex_pdl_ovdu.ovdu_allocation_record表
def clue_ass():
    r=requests.post(host_coll+'/api/insecure/task/clue/ass')
    print(r.json())
#案件分配
def case_ass():
    r=requests.post(host_coll+'/api/insecure/task/case/ass')
    print(r.json())
if __name__ == '__main__':
    sync()
    # recycle()
    # clue_ass()
    # case_ass()
