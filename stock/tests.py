import datetime

from django.test import TestCase

from stock.model.index_info_model import index_info
from stock.service import index_info_service


# Create your tests here.
class stock(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index_info_add_index_info(self):
        print('开始执行--add_index_info--')
        str_start_date = '2005-01-04'
        date_start_date = datetime.datetime.strptime(str_start_date, '%Y-%m-%d').date()
        str_last_update_date = '2005-01-04'
        date_last_update_date = datetime.datetime.strptime(str_last_update_date, '%Y-%m-%d').date()
        new_index_info = index_info.objects.create(index_code='000016.XSHG', index_name='上证50指数', index_data_table='000016.XSHG',
                            index_data_fund='', start_date=date_start_date, last_update_date=date_last_update_date, data_source="jqdata")
        print(new_index_info.index_code)
        print('add_index_info-执行结束')

        print('开始执行--get_all_index_info--')
        index_info_list = index_info_service.get_all_index_info()
        print("test_index_info_get_all_index_info:" + index_info_list[0].index_code)
        detester = index_info_list[0].last_update_date.strftime('%Y-%m-%d')
        print("test_index_info_get_all_index_info:" + detester)
        print('get_all_index_info-执行结束')

        print('开始执行--update_index_info--')
        str_last_update_date = '2020-03-14'
        date_last_update_date = datetime.datetime.strptime(str_last_update_date, '%Y-%m-%d').date()
        index_info.objects.filter(index_code='000016.XSHG').update(last_update_date=date_last_update_date)
        index_info_list = index_info_service.get_all_index_info()
        print("test_index_info_get_all_index_info:" + index_info_list[0].index_code)
        detester = index_info_list[0].last_update_date.strftime('%Y-%m-%d')
        print("test_index_info_get_all_index_info:" + detester)
        self.assertEquals(str_last_update_date, detester)
        print('get_all_index_info执行结束')

        print('开始执行--delete_index_info--')
        index_info.objects.filter(index_code='000016.XSHG').delete()
        index_info_list = index_info_service.get_all_index_info()
        self.assertEquals(len(index_info_list), 0)
        print('delete_index_info-执行结束')

