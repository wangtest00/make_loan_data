import datetime

def get_date_list(start_date, end_date):
    """
    根据开始日期、结束日期返回这段时间里所有天的集合
    :param start_date: 开始日期(日期格式或者字符串格式)
    :param end_date: 结束日期(日期格式或者字符串格式)
    :param format: 格式化字符串, 如: '%Y-%m-%d'
    :return:
    """
    date_list = []
    if isinstance(start_date, str) and isinstance(end_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
        end_date = datetime.datetime.strptime(end_date, '%Y%m%d')
    date_list.append(start_date.strftime('%Y%m%d'))
    while start_date < end_date:
        start_date += datetime.timedelta(days=1)
        date_list.append(start_date.strftime('%Y%m%d'))
    #print(date_list)
    return date_list

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
    if datestart < dateend:
        # 日期叠加一天
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y%m%d'))
        print(date_list)
        return date_list
    # elif datestart==dateend:
    #     print(date_list)
    #     return date_list
    else:
        print('开始日期不能大于结束日期，不运行批量')
        return 0

if __name__ == '__main__':
    get_date_list('20220415','20220415')