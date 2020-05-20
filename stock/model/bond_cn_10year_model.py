# -*- coding: utf-8 -*-
# @Time    : 2020-05-19 19:19
# @Author  : Dingzh.tobest
# 文件描述  ：10年期国债收益率数据

from django.db import models

class bond_cn_10year(models.Model):
    trade_date = models.DateField(null=False, primary_key=True)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    pe_ttm = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'bond.cn.10year'