# -*- coding: utf-8 -*-
# @Time    : 2020-05-19 19:29
# @Author  : Dingzh.tobest
# 文件描述  ： 获取中国债券相关数据

from stock.model.bond_cn_10year_model import bond_cn_10year
from django.db.models import Max
from datacollector import bond
import pandas as pd

def get_bond_cn_10year_history_data():
    return pd.DataFrame(list(bond_cn_10year.objects.all().values()))

def get_bond_cn_10year_last_update_date():
    return bond_cn_10year.objects.aggregate(Max('trade_date'))['trade_date__max']

def get_china_10year_bond_yield_data():
    df, msg = bond.get_china_10year_bond_yield_data()
    return df,msg

def add_bond_cn_10year_yield_date(trade_date, open, high, low, close, pe_ttm):
    return bond_cn_10year.objects.create(trade_date=trade_date, open=open, high=high,low=low, close=close,pe_ttm=pe_ttm)