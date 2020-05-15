# -*- coding: utf-8 -*-
# @Time    : 2020-05-13 12:28
# @Author  : Dingzh.tobest
# 文件描述  ：

from TimingTasks.model.index_stocks_model import index_stocks_model
from django.db.models import Max

def get_index_stocks_byCode(code, trade_date):
    return index_stocks_model.objects.filter(index_code__exact=code, trade_date__exact=trade_date)

def get_last_update_date(code):
    index_stocks = index_stocks_model.objects.filter(index_code__exact=code).aggregate(Max('trade_date'))
    return index_stocks['trade_date__max']

def add_index_info(index_code, index_name, trade_date, index_stocks_str):
    return index_stocks_model.objects.create(index_code=index_code, index_name=index_name, trade_date=trade_date, index_stocks=index_stocks_str)
