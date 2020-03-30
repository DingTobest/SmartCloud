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

    # engine = create_engine('mysql+pymysql://root:root@140.143.154.20/sc_stock?charset=utf8')

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
    # import_history_csv('000016.XSHG', 'd:\\sz50.csv')
    # import_history_csv('000905.XSHG', 'd:\\zz500.csv')
    # import_history_csv('QZZS.SC', 'd:\\szzs.csv')
    import_history_csv('399673.XSHE', 'D:\\historyanalysisdata\\chuangyeban50.399673.XSHE.csv')
    import_history_csv('399006.XSHE', 'D:\\historyanalysisdata\\chuangyebanzhishu.399006.XSHE.csv')
    import_history_csv('000300.XSHG', 'D:\\historyanalysisdata\\hushen300.000300.XSHG.csv')
    import_history_csv('000992.XSHG', 'D:\\historyanalysisdata\\quanzhijinrong.000992.XSHG.csv')
    import_history_csv('000993.XSHG', 'D:\\historyanalysisdata\\quanzhixinxi.000993.XSHG.csv')
    import_history_csv('000991.XSHG', 'D:\\historyanalysisdata\\quanzhiyiyao.000991.XSHG.csv')
    import_history_csv('000807.XSHG', 'D:\\historyanalysisdata\\shipinyinliao.000807.XSHG.csv')
    import_history_csv('399610.XSHE', 'D:\\historyanalysisdata\\tmt50.399610.XSHE.csv')
    import_history_csv('399550.XSHE', 'D:\\historyanalysisdata\\yangshi50.399550.XSHE.csv')
    import_history_csv('000852.XSHG', 'D:\\historyanalysisdata\\zhongzheng1000.000852.XSHG.csv')
    import_history_csv('000922.XSHG', 'D:\\historyanalysisdata\\zhongzhenghongli.000922.XSHG.csv')
    import_history_csv('399967.XSHE', 'D:\\historyanalysisdata\\zhongzhengjungong.399967.XSHE.csv')
    import_history_csv('399812.XSHE', 'D:\\historyanalysisdata\\zhongzhengyanglao.399812.XSHE.csv')
    import_history_csv('399417.XSHE', 'D:\\historyanalysisdata\\国证新能源汽车指数.399417.XSHE.csv')
    import_history_csv('000990.XSHG', 'D:\\historyanalysisdata\\全指消费.000990.XSHG.csv')