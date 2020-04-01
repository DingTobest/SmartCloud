# -*- coding: utf-8 -*-
# @Time    : 2020-03-15 16:39
# @Author  : Dingzh.tobest
# 文件描述  ：历史数据文件导入
import pandas as pd
from sqlalchemy import create_engine

def import_history_csv(table_name, csv_file_path):
    print(csv_file_path)
    index_cp_df = pd.read_csv(csv_file_path, parse_dates=[0])
    index_cp_df['open'] = index_cp_df['open'].round(2)
    index_cp_df['high'] = index_cp_df['high'].round(2)
    index_cp_df['low'] = index_cp_df['low'].round(2)
    index_cp_df['close'] = index_cp_df['close'].round(2)
    index_cp_df['pe_ttm'] = index_cp_df['pe_ttm'].round(2)
    index_cp_df['pb_ttm'] = index_cp_df['pb_ttm'].round(2)
    index_cp_df['ps_ttm'] = index_cp_df['ps_ttm'].round(2)
    index_cp_df.rename(columns={'Unnamed: 0': 'trade_date'}, inplace=True)
    index_cp_df.drop('volume', axis=1, inplace=True)
    index_cp_df.drop('money', axis=1, inplace=True)

    engine = create_engine('mysql+pymysql://root:root@127.0.0.1/sc_stock?charset=utf8')

    drop_table_sql = "DROP TABLE IF EXISTS `%table_name%`;"
    create_table_sql = '''CREATE TABLE `%table_name%` (
          `trade_date` date DEFAULT NULL,
          `open` decimal(10,2) DEFAULT NULL,
          `high` decimal(10,2) DEFAULT NULL,
          `low` decimal(10,2) DEFAULT NULL,
          `close` decimal(10,2) DEFAULT NULL,
          `pe_ttm` decimal(10,2) DEFAULT NULL,
          `pb_ttm` decimal(10,2) DEFAULT NULL,
          `ps_ttm` decimal(10,2) DEFAULT NULL,
          KEY `trade_date` (`trade_date`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

    drop_table_sql = drop_table_sql.replace('%table_name%', table_name)
    create_table_sql = create_table_sql.replace('%table_name%', table_name)

    engine.execute(drop_table_sql)
    engine.execute(create_table_sql)

    # 存入数据库
    index_cp_df.to_sql(table_name, engine, if_exists='append', index=False)

if __name__ == '__main__':
    # import_history_csv('QZZS.SC', 'd:\\QZZS.SC.csv')
    import_history_csv('000016.XSHG', 'd:\\newdata\\000016.XSHG.csv')
    # import_history_csv('000905.XSHG', 'd:\\newdata\\000905.XSHG.csv')
    # import_history_csv('399673.XSHE', 'D:\\newdata\\399673.XSHE.csv')
    # import_history_csv('399006.XSHE', 'D:\\newdata\\399006.XSHE.csv')
    # import_history_csv('000300.XSHG', 'D:\\newdata\\000300.XSHG.csv')
    # import_history_csv('000992.XSHG', 'D:\\newdata\\000992.XSHG.csv')
    # import_history_csv('000993.XSHG', 'D:\\newdata\\000993.XSHG.csv')
    # import_history_csv('000991.XSHG', 'D:\\newdata\\000991.XSHG.csv')
    # import_history_csv('000807.XSHG', 'D:\\newdata\\000807.XSHG.csv')
    # import_history_csv('399610.XSHE', 'D:\\newdata\\399610.XSHE.csv')
    # import_history_csv('399550.XSHE', 'D:\\newdata\\399550.XSHE.csv')
    # import_history_csv('000852.XSHG', 'D:\\newdata\\000852.XSHG.csv')
    # import_history_csv('000922.XSHG', 'D:\\newdata\\000922.XSHG.csv')
    # import_history_csv('399967.XSHE', 'D:\\newdata\\399967.XSHE.csv')
    # import_history_csv('399812.XSHE', 'D:\\newdata\\399812.XSHE.csv')
    # import_history_csv('399417.XSHE', 'D:\\newdata\\399417.XSHE.csv')
    # import_history_csv('000990.XSHG', 'D:\\newdata\\000990.XSHG.csv')