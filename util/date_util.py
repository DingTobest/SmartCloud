# -*- coding: utf-8 -*-
# @Time    : 2020-05-23 9:41
# @Author  : Dingzh.tobest
# 文件描述  ： 处理日期的公共类

# -*- coding: utf-8 -*-
"""
@author: tz_zs
"""
import calendar
from datetime import datetime
from datetime import timedelta

# 判断是否为指数成分股调整日
def check_Constituent_adjustment_day(trade_date):
    year = int(str(trade_date)[0:4])
    first_weekday_6, last_weekday_6 = get_first_and_last_weekday(year, 6, n=3, w="monday")
    first_weekday_12, last_weekday_12 = get_first_and_last_weekday(year, 12, n=3, w="monday")
    if str(first_weekday_6.date()) == trade_date or str(first_weekday_12.date()) == trade_date:
        return True
    else:
        return False

def get_weekday(datetime_obj, week_day="monday"):
    """
    获取指定时间的当周的星期x
    :param datetime_obj: 时间
    :param week_day: 指定的星期x
    :return:
    """
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"), range(7)))  # datetime 模块中，星期一到星期天对应数字 0 到 6
    delta_hour = timedelta(days=1)  # 改变幅度为 1 天
    while datetime_obj.weekday() != d.get(week_day):
        if datetime_obj.weekday() > d.get(week_day):
            datetime_obj -= delta_hour
        elif datetime_obj.weekday() < d.get(week_day):
            datetime_obj += delta_hour
        else:
            pass
    return datetime_obj


def get_first_and_last_weekday(year, month, n=1, w="monday"):
    """
    获取 year 年，month 月 的第n个星期w和倒数第n个星期w的日期
    :param year: 指定年份，如 2019
    :param month: 指定月份，如 6
    :param n: 第n个
    :param w: 指定的星期w
    :return:
    """
    # 获取第一和最后一天
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"), range(7)))  # datetime 模块中，星期一到星期天对应数字 0 到 6
    weekday, count_day = calendar.monthrange(year=year, month=month)  # 返回指定月份第一天（即1号）的星期日期，和本月的总天数 https://blog.csdn.net/tz_zs/article/details/86629959
    first_day = datetime(year=year, month=month, day=1)  # <type 'datetime.datetime'>
    last_day = datetime(year=year, month=month, day=count_day)
    # first_day, last_day = get_month_firstday_and_lastday(year=year, month=month, n=1)

    # 第1个星期w
    if first_day.weekday() > d.get(w):  # 说明本周的星期w在上个月
        datetime_obj = first_day + timedelta(weeks=1)
    else:
        datetime_obj = first_day
    datetime_obj += timedelta(weeks=n - 1)
    first_weekday = get_weekday(datetime_obj=datetime_obj, week_day=w)

    # 倒数第1个星期w
    if last_day.weekday() < d.get(w):  # 说明本周的星期w在下一个月
        datetime_obj = last_day - timedelta(weeks=1)
    else:
        datetime_obj = last_day
    datetime_obj -= timedelta(weeks=n - 1)
    last_weekday = get_weekday(datetime_obj=datetime_obj, week_day=w)

    return first_weekday, last_weekday

if __name__ == '__main__':
    print(check_Constituent_adjustment_day('2020-06-15'))
    print(check_Constituent_adjustment_day('2019-12-16'))
    print(check_Constituent_adjustment_day('2020-05-22'))
