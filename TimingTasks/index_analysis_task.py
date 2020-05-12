# -*- coding: utf-8 -*-
# @Time    : 2020-03-17 16:33
# @Author  : Dingzh.tobest
# 文件描述  ：计算指数PE、PB、PS的定时任务，写入到数据库当中

import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCloud.settings')
django.setup()

# from django.db import connection
from sqlalchemy import create_engine
from stock import index_info_service
from stock.index_analysis_service import index_analysis
from sctk import data_util
from sctk import index_fundamental_analysis
from django.conf import settings

# 计算指数相关的定时任务
def calc_index_analysis_info():
    index_infos = index_info_service.get_all_index_info()

    data_util.data_service_init()

    db_name = settings.DATABASES['default']['NAME']
    host = settings.DATABASES['default']['HOST']
    user = settings.DATABASES['default']['USER']
    password = settings.DATABASES['default']['PASSWORD']

    connect_str = 'mysql+pymysql://' + user + ':' + password + '@' + host + '/' + db_name + '?charset=utf8'
    engine = create_engine(connect_str)
    for index_info in index_infos:
        print('当前进行计算的指数：' + index_info.index_code)
        indexAnalysis = index_analysis(index_info.index_data_table)
        last_update_date = indexAnalysis.get_last_update_date()
        print('上次计算的日期：' + str(last_update_date))
        trade_date_list = data_util.get_trade_date(last_update_date)
        analysis_date_list = trade_date_list
        # print(trade_date_list)
        if analysis_date_list[0] == last_update_date:
            analysis_date_list = analysis_date_list[1:]

        if len(analysis_date_list) == 0:
            continue

        if analysis_date_list[-1] == datetime.date.today():
            analysis_date_list = analysis_date_list[:-1]

        if len(analysis_date_list) > 0:
            index_pe_list = []
            index_pb_list = []
            index_ps_list = []
            for trade_date in analysis_date_list:
                print(trade_date)
                stocks = data_util.get_index_stocks(index_info.index_code, trade_date)
                df = data_util.get_stocks_fundamentals(stocks, trade_date)
                index_pe = index_fundamental_analysis.calc_index_pe_ttm(df)
                index_pb = index_fundamental_analysis.calc_index_pb_ttm(df)
                index_ps = index_fundamental_analysis.calc_index_ps_ttm(df)
                print('index_pe' + str(round(index_pe,2)))
                print('index_pb' + str(round(index_pb,2)))
                print('index_ps' + str(round(index_ps,2)))
                index_pe_list.append(round(index_pe,2))
                index_pb_list.append(round(index_pb, 2))
                index_ps_list.append(round(index_ps, 2))

            index_new_df = data_util.get_index_price_data(index_info.index_code, analysis_date_list[0], analysis_date_list[-1])
            index_new_df['pe_ttm'] = index_pe_list
            index_new_df['pb_ttm'] = index_pb_list
            index_new_df['ps_ttm'] = index_ps_list
            index_new_df.reset_index(inplace=True)
            index_new_df.rename(columns={'index': 'trade_date'}, inplace=True)

            print(index_new_df)
            print(index_info.index_data_table)

            index_new_df.to_sql(index_info.index_data_table.lower(), con=engine, if_exists='append', index=False)
            # index_new_df.to_sql(index_info.index_data_table, con=connection, if_exists='append', index=False)

    return 'success'

if __name__ == '__main__':
    print(settings.DATABASES['default']['NAME'])
    print(settings.DATABASES['default']['HOST'])
    print(settings.DATABASES['default']['PORT'])
    print(settings.DATABASES['default']['USER'])
    print(settings.DATABASES['default']['PASSWORD'])