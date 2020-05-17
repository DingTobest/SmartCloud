# -*- coding: utf-8 -*-
# @Time    : 2020-05-13 12:02
# @Author  : Dingzh.tobest
# 文件描述  ： 指数成分股

from django.db import models

class index_stocks_model(models.Model):
    id = models.AutoField(primary_key=True)
    index_code = models.CharField(null=False, max_length=16, db_index=True)
    index_name = models.CharField(null=False, max_length=32)
    trade_date = models.DateField(null=False, db_index=True)
    index_stocks = models.TextField(null=False)

    class Meta:  # 元信息类
        db_table = 'index_stocks'  # 自定义表的名字
