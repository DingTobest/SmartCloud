from django.test import TestCase
from TimingTasks.service import data_record_task_service
from TimingTasks.service import index_stocks_service
import pandas as pd

class data_record(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index_stocks(self):
        file_path = 'D:\\SmartCloudFuture\\SmartCloud\\TimingTasks\\downloadfile\\931087.CIS.2020-05-13.xls'
        df = pd.read_excel(file_path)
        df['sys_code'] = df['成分券代码Constituent Code'].map(str) + '.' + df['交易所Exchange']
        index_stocks_str = ','.join(list(df['sys_code']))
        index_stocks_str = index_stocks_str.replace('.SHH', '.XSHG')
        index_stocks_str = index_stocks_str.replace('.SHZ', '.XSHE')

        trade_date = df['日期Date'].iloc[0]

        index_stocks_service.add_index_info('931087.CSI', '中证科技龙头指数', trade_date, index_stocks_str)

        index_list = index_stocks_service.get_index_stocks_byCode('931087.CSI', trade_date)
        print(index_list[0].index_stocks)