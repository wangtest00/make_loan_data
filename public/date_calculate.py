import datetime

# 获取指定日期间隔内的日期列表
def create_assist_date(datestart=None, dateend=None):
    """
    获取指定日期间隔内的日期列表
    :param datestart: 开始日期 ---> str
    :param dateend: 结束日期 ---> str
    :return: 日期列表 ['2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28',...]
    """
    if datestart is None:
        datestart = '20191228'
    if dateend is None:
        dateend = datetime.datetime.now().strftime('%Y%m%d')
    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y%m%d')
    dateend = datetime.datetime.strptime(dateend, '%Y%m%d')
    date_list = []
    date_list.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y%m%d'))
    #print(date_list)
    return date_list

if __name__ == '__main__':
    create_assist_date('20211026','20211026')