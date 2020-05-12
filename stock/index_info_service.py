# -*- coding: utf-8 -*-
# @Time    : 2020-03-15 10:57
# @Author  : Dingzh.tobest
# 文件描述  ：

from stock.model.index_info_model import index_info

def get_all_index_info():
    return index_info.objects.all()
    # return index_info.objects.order_by('id')

def add_index_info(index_code, index_name, index_date_table, index_data_fund, start_date, last_update_date):
    return index_info.objects.create(index_code=index_code, index_name=index_name, index_date_table=index_date_table,
                        index_data_fund=index_data_fund, start_date=start_date, last_update_date=last_update_date)
