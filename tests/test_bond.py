# -*- coding: utf-8 -*-
# @Time    : 2020-05-19 17:40
# @Author  : Dingzh.tobest
# 文件描述  ：

from datacollector import bond
import unittest

class TestBond(unittest.TestCase):
    def test_get_china_10year_bond_yield_data(self):
        df, msg = bond.get_china_10year_bond_yield_data()
        print(df)
        assert (len(df) >= 10)
