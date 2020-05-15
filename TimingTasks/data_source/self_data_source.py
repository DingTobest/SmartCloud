# -*- coding: utf-8 -*-
# @Time    : 2020-05-13 9:49
# @Author  : Dingzh.tobest
# 文件描述  ：独立的数据源，获取数据库中的数据
from TimingTasks.service import index_stocks_service

# 通过爬虫获取数据存放在数据库中，通过数据库读取相关的指数成分股
def get_index_stocks(code, trade_date):
    index_list = index_stocks_service.get_index_stocks_byCode(code, trade_date)
    return index_list[0].index_stocks.split(',')