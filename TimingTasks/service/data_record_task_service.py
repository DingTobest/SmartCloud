# -*- coding: utf-8 -*-
# @Time    : 2020-05-13 10:09
# @Author  : Dingzh.tobest
# 文件描述  ： 通过爬虫获取相关金融数据

import requests
import sys
import os
import pandas as pd
from TimingTasks.service import index_stocks_service

# 从中金所网站上爬取成分股数据
def get_index_stocks_from_cis(code, name):
    file_path = sys.path[0] + '\\TimingTasks\\downloadfile\\' + code + '.xls'
    if os.path.exists(file_path):
        os.remove(file_path)
        print('删除旧的历史文件：' + file_path)

    temp_code = code[:code.find('.')]
    url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/' +  temp_code + 'cons.xls?'
    r = requests.get(url, stream=True)

    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)

    f.close()

    df = pd.read_excel(file_path, converters = {'成分券代码Constituent Code': str})
    df['sys_code'] = df['成分券代码Constituent Code'].map(str) + '.' + df['交易所Exchange']
    index_stocks_str = ','.join(list(df['sys_code']))
    index_stocks_str = index_stocks_str.replace('.SHH', '.XSHG')
    index_stocks_str = index_stocks_str.replace('.SHZ', '.XSHE')

    trade_date = df['日期Date'].iloc[0]

    index_stocks_service.add_index_info(code, name, trade_date, index_stocks_str)

    mem_path = sys.path[0] + '\\TimingTasks\\downloadfile\\' + code + '.' + trade_date + '.xls'
    if os.path.exists(file_path):
        os.rename(file_path, mem_path)

    if os.path.exists(file_path):
        os.remove(file_path)
        print('删除本次更新文件：' + mem_path)

if __name__ == '__main__':
    get_index_stocks_from_cis('931087.CSI', '中证科技龙头指数')