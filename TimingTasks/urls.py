# -*- coding: utf-8 -*-
# @Time    : 2019-12-19 12:00
# @Author  : Dingzh.tobest
# 文件描述  ：

from django.conf.urls import url, include
import TimingTasks.views

urlpatterns = [
    url(r'calc_index_analysis_info', TimingTasks.views.calc_index_analysis_info, ),
    url(r'download_index_stocks', TimingTasks.views.download_index_stocks, ),
    url(r'download_bonds_yield', TimingTasks.views.download_bonds_yield, ),
]