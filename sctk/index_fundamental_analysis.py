# -*- coding: utf-8 -*-
# @Time    : 2020-02-10 14:38
# @Author  : Dingzh.tobest
# 文件描述  ：用于计算相关指数相关指标

# 计算指数市盈率(PE)
# df中包含所有股票的pe_ttm信息
# 计算方法：过滤调亏损股票（市盈率小于0），对剩余股票市盈率取中位数
# 通过中位数的形式，衡量市场主体估值水平
def calc_index_pe_ttm(df):
    df_pe = df[df['pe_ratio'] > 0]
    index_pe = df_pe['pe_ratio'].median()
    return index_pe

# 计算指数市净率(PB)
# df中包含所有股票的pb_ttm信息
# 计算方法：过滤调亏损股票（市净率小于0），对剩余股票市净率取中位数
# 通过中位数的形式，衡量市场主体估值水平
def calc_index_pb_ttm(df):
    df_pb = df[df['pb_ratio'] > 0]
    index_pb = df_pb['pb_ratio'].median()
    return index_pb

# 计算指数市销率(PS)
# df中包含所有股票的ps_ttm信息
# 计算方法：过滤调亏损股票（市销率小于0），对剩余股票市销率取中位数
# 通过中位数的形式，衡量市场主体估值水平
def calc_index_ps_ttm(df):
    df_ps = df[df['ps_ratio'] > 0]
    index_ps = df_ps['ps_ratio'].median()
    return index_ps

# 暂时废弃以下计算方式
# 以下计算方式会导致低市盈率股票的权重过大，计算出来的市盈率过小，不符合对指数市盈率的观察需求

# 计算指数市盈率(PE)
# df中包含所有股票的pe_ttm信息
# 计算方法：对所有个股的pe_ttm数据取倒数，剔除掉小于0的数据，通过总和除以所有的股票数，再取倒数，形成指数pe_ttm
# 通过取倒数的形式，大大减小了超高PE的股票对指数PE的影响
def calc_index_pe_ttm_old(df):
    df['r_pe_ttm'] = 1 / df['pe_ratio']
    df2 = df[df['r_pe_ttm'] > 0]
    r_index_pe = df2['r_pe_ttm'].sum() / len(df)
    index_pe = 1 / r_index_pe
    return index_pe

# 计算指数市净率(PB)
# df中包含所有股票的pb_ttm信息
# 计算方法：对所有个股的pb_ttm数据取倒数，剔除掉小于0的数据，通过总和除以所有的股票数，再取倒数，形成指数pb_ttm
# 通过取倒数的形式，大大减小了超高PB的股票对指数PB的影响
def calc_index_pb_ttm_old(df):
    df['r_pb_ttm'] = 1 / df['pb_ratio']
    df2 = df[df['r_pb_ttm'] > 0]
    r_index_pb = df2['r_pb_ttm'].sum() / len(df)
    index_pb = 1 / r_index_pb
    return index_pb

# 计算指数市销率(PS)
# df中包含所有股票的ps_ttm信息
# 计算方法：对所有个股的ps_ttm数据取倒数，剔除掉小于0的数据，通过总和除以所有的股票数，再取倒数，形成指数ps_ttm
# 通过取倒数的形式，大大减小了超高PS的股票对指数PB的影响
def calc_index_ps_ttm_old(df):
    df['r_ps_ttm'] = 1 / df['ps_ratio']
    df2 = df[df['r_ps_ttm'] > 0]
    r_index_ps = df2['r_ps_ttm'].sum() / len(df)
    index_ps = 1 / r_index_ps
    return index_ps