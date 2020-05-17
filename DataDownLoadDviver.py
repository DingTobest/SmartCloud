# -*- coding: utf-8 -*-
# @Time    : 2020-05-17 12:28
# @Author  : Dingzh.tobest
# 文件描述  ： 用于数据下载的程序


import requests
import json
import os

import sys

host_address = 'http://127.0.0.1:8000'

# 调用每日成分股下载的服务
def download_index_stocks():
    addr = host_address + '/timingtask/download_index_stocks'
    r = requests.post(addr)
    if r.status_code == 200:
        result = json.loads(r.text)
        print(result)
    else:
        raise Exception('更新每日数据接口【download_index_stocks】调用失败')

if __name__ == '__main__':
    download_index_stocks()