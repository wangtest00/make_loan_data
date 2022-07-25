import requests
import time

header={'Accept':'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh,zh-CN;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection': 'keep-alive',
'Cookie': 'wt_aid=2414c070-8ca1-4df8-80fd-869b742d19fa; gr_user_id=3c2d111b-45d5-4ae1-a06f-c068a5fa267a; AGL_USER_ID=6d29ce4d-b2b8-419b-8c73-88208a938740; s-5f34cf9b8552f79ad949d273=cf89084e58634bc7aa5445f8ae80adf5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%227e718045a98b455486aa2babbcd584d7%22%2C%22first_id%22%3A%2218214821bbd33e-0f444444444445-1f343371-1327104-18214821bbe127a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2218214821bbd33e-0f444444444445-1f343371-1327104-18214821bbe127a%22%7D',
'Host': 'quantstack.pingcode.com',
'Referer': 'https://quantstack.pingcode.com/workspace/dashboards/5ff2f731afa9fe001738acd9',
'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'sentry-trace': 'ff2ec5cc0f984638bb8015795bdfb0f7-a6905d45bb68f53a-1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}

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
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI3ZTcxODA0NWE5OGI0NTU0ODZhYTJiYWJiY2Q1ODRkNyIsInRlYW1faWQiOiI1ZjM0Y2Y5Yjg1NTJmNzlhZDk0OWQyNzMiLCJpYXQiOjE2NTg3MTk3NjJ9.3ak1BcRdNKGLrWU9x5jjHqfumBrOpcJCWsz3RVOsg0s',
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
    print(t)
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
    r=requests.get("https://quantstack.pingcode.com/api/agile/projects/5f34d1a73fa4b651a03b4a48/scrum/release/work-item/related-work-items?version_id="+version_id+"&sort_by=type&sort_type=1&t=1658730719514",headers=header)
    #print(r.url)
    t=r.json()
    data=t['data']['value']
    data_list=[]
    for data in data:
        print(data['title'])
        data_list.append(data['title'])
    print(data_list)


    #print(sum)
if __name__ == '__main__':
    get_work_item('62b42771648068316fd9f9b5')    #version_id
    #get_notifications()