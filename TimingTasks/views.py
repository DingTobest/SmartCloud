from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from TimingTasks.service import index_analysis_task_service
from stock.service import index_info_service
from TimingTasks.service import data_record_task_service
from TimingTasks.service import data_service
from TimingTasks.service import index_stocks_service

import datetime


@require_http_methods(["POST"])
def calc_index_analysis_info(request):
    response = {}
    response['result'] = index_analysis_task_service.calc_index_analysis_info()

    return JsonResponse(response)

@require_http_methods(["POST"])
def download_index_stocks(request):
    index_info_list = index_info_service.get_tushare_index_info()

    data_service.data_service_init()

    update_code = ''

    for index_info in index_info_list:
        print('当前计算的指数代码：' + index_info.index_code)
        last_update_date = index_stocks_service.get_last_update_date(index_info.index_code)

        print('上次计算的日期：' + str(last_update_date))

        trade_date_list = data_service.get_trade_date(last_update_date)

        analysis_date_list = trade_date_list

        if len(analysis_date_list) == 0:
            continue

        if analysis_date_list[0] == last_update_date:
            analysis_date_list = analysis_date_list[1:]

        if analysis_date_list[-1] == datetime.date.today():
            analysis_date_list = analysis_date_list[:-1]

        if len(analysis_date_list) == 0:
            break

        print('当前处理的指数为：' + index_info.index_code)
        data_record_task_service.get_index_stocks_from_cis(index_info.index_code, index_info.index_name)

        update_code = update_code + ',' + index_info.index_code

    response = {}
    response['result'] = 'success'
    response['update_code'] = update_code

    return JsonResponse(response)