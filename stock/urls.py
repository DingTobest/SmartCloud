# -*- coding: utf-8 -*-
# @Time    : 2019-12-19 12:00
# @Author  : Dingzh.tobest
# 文件描述  ：

from django.conf.urls import url, include
import stock.views

urlpatterns = [
    url(r'add_stock_info', stock.views.add_stock_info, ),
    url(r'get_stock_info', stock.views.get_stock_info, ),
    url(r'get_index_analysis_info', stock.views.get_index_analysis_info, ),
    url(r'get_all_index_analysis_data', stock.views.get_all_index_analysis_data, ),
]