# -*- coding: utf-8 -*-
# @Time    : 2020-02-10 10:56
# @Author  : Dingzh.tobest
# 文件描述  ： 为指标计算提供数据服务

import sys
import json
import jqdatasdk
import tushare as ts
from TimingTasks.data_source import self_data_source

JQDATA_USER = ''
JQDATA_PASSWORD = ''
TUSHARE_TOKEN = ''

pro_api = None

# 初始化数据服务
def data_service_init():
    config_file_path = sys.path[0] + '\\TimingTasks\\config.json'
    config = open(config_file_path)
    setting = json.load(config)

    JQDATA_USER = setting['JQDATA_USER']
    JQDATA_PASSWORD = setting['JQDATA_PASSWORD']
    TUSHARE_TOKEN = setting['TUSHARE_TOKEN']

    jqdatasdk.auth(JQDATA_USER, JQDATA_PASSWORD)
    ts.set_token(TUSHARE_TOKEN)
    global pro_api
    pro_api = ts.pro_api(TUSHARE_TOKEN)


# 获取国内市场交易日
# start_date：开始日期
def get_trade_date(start_date):
    trade_date_list = jqdatasdk.get_trade_days(start_date)
    return trade_date_list

# 获取指数相关成分股
# code：指数代码
# trade_date：交易日期
def get_index_stocks(code, trade_date, data_source):
    # 通过深证综指399106.XSHE来观察全市场数据
    stocks = []
    # 主要数据从JQData进行获取
    if data_source == 'jqdata':
        if code == '399106.XSHE':
            stocks = list(jqdatasdk.get_all_securities(date=trade_date).index)
        else:
            stocks = jqdatasdk.get_index_stocks(code, trade_date)
    # 通过tushare提供其他不包含数据
    elif data_source == 'tushare':
        stocks = self_data_source.get_index_stocks(code, trade_date)
    return stocks

# 获取个股PE、PB、PS的信息
# stocks：股票集合
# trade_date：交易日期
def get_stocks_fundamentals(stocks, trade_date):
    q = jqdatasdk.query(jqdatasdk.valuation).filter(jqdatasdk.valuation.code.in_(stocks))
    df = jqdatasdk.get_fundamentals(q, trade_date)
    return df

def get_index_price_data(index_code, start_date, end_date, data_source):
    if data_source == 'jqdata':
        df = jqdatasdk.get_price(index_code, start_date=start_date, end_date=end_date,fields=['open', 'close', 'high', 'low'], frequency='daily')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'trade_date'}, inplace=True)
    elif data_source == 'tushare':
        start_date2 = str(start_date).replace('-', '')
        end_date2 = str(end_date).replace('-', '')
        df = pro_api.index_daily(ts_code=index_code, start_date=start_date2, end_date=end_date2)
        df.drop(['ts_code','vol','amount','pre_close', 'change', 'pct_chg'], axis=1, inplace = True)
        df['open'] = df['open'].round(2)
        df['high'] = df['high'].round(2)
        df['low'] = df['low'].round(2)
        df['close'] = df['close'].round(2)
    return df

if __name__ == '__main__':
    data_service_init()