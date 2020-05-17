# -*- coding: utf-8 -*-
# @Time    : 2020-03-15 15:45
# @Author  : Dingzh.tobest
# 文件描述  ： 指数数据计算的数据表
from django.db import connection
import pandas as pd

class index_analysis(object):

    def __init__(self, index_code):
        self.index_code = index_code
        self.last_analysis_date = None
        self.index_analysis_df = None
        self.history_max_pe = 0
        self.history_min_pe = 0
        self.pe_ttm_now = 0
        self.pe_ttm_percentage = ''
        self.pe_ttm_percentage_5y = ''
        self.pe_ttm_percentage_10y = ''

        self.pb_ttm_now = 0
        self.pb_ttm_percentage = ''
        self.pb_ttm_percentage_5y = ''
        self.pb_ttm_percentage_10y = ''

        self.ps_ttm_now = 0
        self.ps_ttm_percentage = ''
        self.ps_ttm_percentage_5y = ''
        self.ps_ttm_percentage_10y = ''

        self.last_5Day_data = None

    def get_last_update_date(self):
        cursor = connection.cursor()
        # sql_str = 'select * from `' + self.index_code + '`'
        # index_analysis_df = pd.read_sql(sql_str, connection)
        # return index_analysis_df['trade_date'].iloc[-1]
        sql_str = 'select max(trade_date) from `' + self.index_code + '`'
        last_trade_date = pd.read_sql(sql_str, connection)
        print(type(last_trade_date['max(trade_date)'][0]))
        return last_trade_date['max(trade_date)'].iloc[0]

    def get_index_analysis_info(self):
        cursor = connection.cursor()
        sql_str = 'select * from `' + self.index_code + '`'
        self.index_analysis_df = pd.read_sql(sql_str, connection)
        self.index_analysis_df['trade_date'] = self.index_analysis_df['trade_date'].astype(str)

        self.last_analysis_date = self.index_analysis_df['trade_date'].iloc[-1]

        # 【PE】当前数据
        pe_ttm_now = self.index_analysis_df['pe_ttm'].iloc[-1]

        # 当前历史PE百分比
        pe_ttm_percentage = len(self.index_analysis_df[self.index_analysis_df.pe_ttm < pe_ttm_now]) / len(self.index_analysis_df)
        temp = pe_ttm_percentage * 100
        pe_ttm_percentage_str = '%.2f' % temp + '%'

        # 当前5年PE百分比
        if len(self.index_analysis_df) > 1250:
            index_cp_df_5y = self.index_analysis_df[-1250:]
            pe_ttm_percentage_5y = len(index_cp_df_5y[index_cp_df_5y.pe_ttm < pe_ttm_now]) / len(index_cp_df_5y)
            temp = pe_ttm_percentage_5y * 100
            pe_ttm_percentage_5y_str = '%.2f' % temp + '%'
        else:
            pe_ttm_percentage_5y_str = ''

        # 当前10年PE百分比
        if len(self.index_analysis_df) > 2500:
            index_cp_df_10y = self.index_analysis_df[-2500:]
            pe_ttm_percentage_10y = len(index_cp_df_10y[index_cp_df_10y.pe_ttm < pe_ttm_now]) / len(index_cp_df_10y)
            temp = pe_ttm_percentage_10y * 100
            pe_ttm_percentage_10y_str = '%.2f' % temp + '%'
        else:
            pe_ttm_percentage_10y_str = ''

        self.pe_ttm_now = pe_ttm_now
        self.pe_ttm_percentage = pe_ttm_percentage_str
        self.pe_ttm_percentage_5y = pe_ttm_percentage_5y_str
        self.pe_ttm_percentage_10y = pe_ttm_percentage_10y_str

        # 【PB】当前数据
        pb_ttm_now = self.index_analysis_df['pb_ttm'].iloc[-1]
        # 当前历史PB百分比
        pb_ttm_percentage = len(self.index_analysis_df[self.index_analysis_df.pb_ttm < pb_ttm_now]) / len(self.index_analysis_df)
        temp = pb_ttm_percentage * 100
        pb_ttm_percentage_str = '%.2f' % temp + '%'

        # 当前5年PB百分比
        if len(self.index_analysis_df) > 1250:
            index_cp_df_5y = self.index_analysis_df[-1250:]
            pb_ttm_percentage_5y = len(index_cp_df_5y[index_cp_df_5y.pb_ttm < pb_ttm_now]) / len(index_cp_df_5y)
            temp = pb_ttm_percentage_5y * 100
            pb_ttm_percentage_5y_str = '%.2f' % temp + '%'
        else:
            pb_ttm_percentage_5y_str = ''

        # 当前10年PB百分比
        if len(self.index_analysis_df) > 2500:
            index_cp_df_10y = self.index_analysis_df[-2500:]
            pb_ttm_percentage_10y = len(index_cp_df_10y[index_cp_df_10y.pb_ttm < pb_ttm_now]) / len(index_cp_df_10y)
            temp = pb_ttm_percentage_10y * 100
            pb_ttm_percentage_10y_str = '%.2f' % temp + '%'
        else:
            pb_ttm_percentage_10y_str = ''

        self.pb_ttm_now = pb_ttm_now
        self.pb_ttm_percentage = pb_ttm_percentage_str
        self.pb_ttm_percentage_5y = pb_ttm_percentage_5y_str
        self.pb_ttm_percentage_10y = pb_ttm_percentage_10y_str

        # 【PS】当前数据
        ps_ttm_now = self.index_analysis_df['ps_ttm'].iloc[-1]

        # 当前历史PS百分比
        ps_ttm_percentage = len(self.index_analysis_df[self.index_analysis_df.ps_ttm < ps_ttm_now]) / len(self.index_analysis_df)
        temp = ps_ttm_percentage * 100
        ps_ttm_percentage_str = '%.2f' % temp + '%'

        # 当前5年PS百分比
        if len(self.index_analysis_df) > 1250:
            index_cp_df_5y = self.index_analysis_df[-1250:]
            ps_ttm_percentage_5y = len(index_cp_df_5y[index_cp_df_5y.ps_ttm < ps_ttm_now]) / len(index_cp_df_5y)
            temp = ps_ttm_percentage_5y * 100
            ps_ttm_percentage_5y_str = '%.2f' % temp + '%'
        else:
            ps_ttm_percentage_5y_str = ''

        # 当前10年PS百分比
        if len(self.index_analysis_df) > 2500:
            index_cp_df_10y = self.index_analysis_df[-2500:]
            ps_ttm_percentage_10y = len(index_cp_df_10y[index_cp_df_10y.ps_ttm < ps_ttm_now]) / len(index_cp_df_10y)
            temp = ps_ttm_percentage_10y * 100
            ps_ttm_percentage_10y_str = '%.2f' % temp + '%'
        else:
            ps_ttm_percentage_10y_str = ''

        self.history_max_pe = self.index_analysis_df.pe_ttm.max()
        self.history_min_pe = self.index_analysis_df.pe_ttm.min()
        self.ps_ttm_now = ps_ttm_now
        self.ps_ttm_percentage = ps_ttm_percentage_str
        self.ps_ttm_percentage_5y = ps_ttm_percentage_5y_str
        self.ps_ttm_percentage_10y = ps_ttm_percentage_10y_str

        # 近5日数据
        self.last_5Day_data = self.index_analysis_df[-5:].copy()
        self.last_5Day_data.drop('open', axis=1, inplace=True)
        self.last_5Day_data.drop('high', axis=1, inplace=True)
        self.last_5Day_data.drop('low', axis=1, inplace=True)

        return 'success'