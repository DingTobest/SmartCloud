# -*- coding: utf-8 -*-
# @Time    : 2020-02-10 10:56
# @Author  : Dingzh.tobest
# 文件描述  ： 为指标计算提供数据服务

import sys
import json
import jqdatasdk

JQDATA_USER = ''
JQDATA_PASSWORD = ''

# 初始化数据服务
def data_service_init():
    config_file_path = sys.path[0] + '\\sctk\\config.json'
    config = open(config_file_path)
    setting = json.load(config)

    JQDATA_USER = setting['JQDATA_USER']
    JQDATA_PASSWORD = setting['JQDATA_PASSWORD']

    jqdatasdk.auth(JQDATA_USER, JQDATA_PASSWORD)

# 获取国内市场交易日
# start_date：开始日期
def get_trade_date(start_date):
    trade_date_list = jqdatasdk.get_trade_days(start_date)
    return trade_date_list

# 获取指数相关成分股
# code：指数代码
# trade_date：交易日期
def get_index_stocks(code, trade_date):
    # 通过深证综指399106.XSHE来观察全市场数据
    if code == '399106.XSHE':
        stocks = list(jqdatasdk.get_all_securities(date=trade_date).index)
    else:
        stocks = jqdatasdk.get_index_stocks(code, trade_date)
    return stocks

# 获取个股PE、PB、PS的信息
# stocks：股票集合
# trade_date：交易日期
def get_stocks_fundamentals(stocks, trade_date):
    q = jqdatasdk.query(jqdatasdk.valuation).filter(jqdatasdk.valuation.code.in_(stocks))
    df = jqdatasdk.get_fundamentals(q, trade_date)
    return df

def get_index_price_data(index_code, start_date, end_date):
    df = jqdatasdk.get_price(index_code, start_date=start_date, end_date=end_date,fields=['open', 'close', 'high', 'low'], frequency='daily')
    return df

if __name__ == '__main__':
    data_service_init()