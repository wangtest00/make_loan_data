import requests
import time

header={'Accept':'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'Cookie': 'sensorsdata2015jssdkcross={"distinct_id":"7e718045a98b455486aa2babbcd584d7","first_id":"17a8939be7c144-0ff6ddee0a3fa5-d7e1739-1327104-17a8939be7df0f","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":""},"$device_id":"17a8939be7c144-0ff6ddee0a3fa5-d7e1739-1327104-17a8939be7df0f"}; sensorsdata2015jssdkcross={"distinct_id":"7e718045a98b455486aa2babbcd584d7","first_id":"17a8939be7c144-0ff6ddee0a3fa5-d7e1739-1327104-17a8939be7df0f","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":""},"$device_id":"17a8939be7c144-0ff6ddee0a3fa5-d7e1739-1327104-17a8939be7df0f"}; AGL_USER_ID=92001a88-3e24-4cf0-9396-e45360b355ca; s-5f34cf9b8552f79ad949d273=184ad67e799c402983147eb29c620efe; wt_aid=10f28833-5965-4465-900a-58aeb6f0fc61',
'Host': 'quantstack.pingcode.com',
'Referer': 'https://quantstack.pingcode.com/workspace/dashboards/5ff2f731afa9fe001738acd9',
'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'sentry-trace': '6c746120100749baa1bbae987903a8d4-a4d48ab519eadc9f-1',
'User-Agent': 'Mozilla/'}

def get_mywork_list():
    url="https://quantstack.pingcode.com/api/ladon/dashboard/widgets/5ff2f731afa9fe001738acde/content?t=1629181171048"
    r=requests.get(url,headers=header)
    t=r.json()
    print(t)
    t=t['data']['value']
    print('待办工作项总数=',len(t))
    work_list=[]
    for i in range(10,len(t)):
        print(t[i]['title'])
        work_list.append(t[i]['title'])
    print(work_list)
#获取提示消息中，所有关于任务项的名称
def get_notifications():
    timev=str(time.time()*1000000)[:13]
    header2={'Accept':'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3ZTcxODA0NWE5OGI0NTU0ODZhYTJiYWJiY2Q1ODRkNyIsInRlYW1faWQiOiI1ZjM0Y2Y5Yjg1NTJmNzlhZDk0OWQyNzMiLCJpYXQiOjE2MjkxODI0ODF9.i1xUWsSwCfYpwG-1td5FJVvGylmIySpXGeQOGU5ZSt0',
        'Host': 'iris.pingcode.com',
        'Referer': 'https://quantstack.pingcode.com/workspace/dashboards/5ff2f731afa9fe001738acd9',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'sentry-trace': '6c746120100749baa1bbae987903a8d4-a4d48ab519eadc9f-1',
        'User-Agent': 'Mozilla/'}
    url2="https://iris.pingcode.com/api/iris/notifications/recent?t="+timev
    r2=requests.get(url2,headers=header2)
    t=r2.json()
    t=t['data']['value']
    print(t)
    for i in range(len(t)):
        #print(t[i]['object'])
        if t[i]['object']['type']=='task':  #只筛选出任务类型的数据，排除story,bug
            print(t[i]['object']['name'])
        else:
            pass

#获取某个版本下，所有测试相关的任务项，并且组装
def get_work_item(version_id):
    r=requests.get('https://quantstack.pingcode.com/api/agile/projects/5f34d1a73fa4b651a03b4a48/scrum/release/work-item/related-work-items?'
                   'version_id='+version_id+'&sort_by=type&sort_type=1&t=1634897835071 HTTP/1.1',headers=header)
    print(r.content)
    t=r.json()
    t=t['data']['value']
    sum=[]
    for i in range(len(t)):
        #print(t[i])
        r=requests.get("https://quantstack.pingcode.com/api/agile/work-items/"+t[i]['_id']+"/children?t=1634898646091",headers=header)
        s=r.json()
        s=s['data']['value']
        #print(s)
        muban=[]
        for j in range(len(s)):
            #print(s[j])
            if '测试' in s[j]['title']:
                print(str(i)+"."+s[j]['title']+"-进度100%")
                muban.append(str(str(i)+"."+s[j]['title']+"-进度100%"))
                sum.append(muban)
            else:
                pass
    #print(sum)
if __name__ == '__main__':
    get_work_item('6204c9e1eeb701ff8d1f5d38')    #version_id
    #get_notifications()