import datetime
import json
import sys
import pandas as pd

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from stock.model.index_info_model import index_info
from stock.service.index_analysis_service import index_analysis
from stock.service import bond_cn_service


# Create your views here.

@require_http_methods(["POST"])
def add_stock_info(request):
    add_info = json.loads(request.body)

    new_index_code = add_info.get('index_code')
    new_index_name = add_info.get('index_name')
    new_index_data_table = add_info.get('index_data_table')
    new_index_data_fund = add_info.get('index_data_fund')
    new_start_date = add_info.get('start_date')
    new_last_update_date = add_info.get('last_update_date')
    new_data_source = add_info.get('data_source')

    str_start_date = new_start_date
    date_start_date = datetime.datetime.strptime(str_start_date, '%Y-%m-%d').date()
    str_last_update_date = new_last_update_date
    date_last_update_date = datetime.datetime.strptime(str_last_update_date, '%Y-%m-%d').date()

    new_index_info = index_info.objects.create(index_code=new_index_code, index_name=new_index_name,
                                               index_data_table=new_index_data_table,
                                               index_data_fund=new_index_data_fund, start_date=new_start_date,
                                               last_update_date=new_last_update_date,
                                               data_source=new_data_source)

    response = {}
    response['msg'] = 'success'
    response['error_num'] = 0

    return JsonResponse(response)

@require_http_methods(["GET"])
def get_stock_info(request):
    response = {}
    response['msg'] = 'success'
    response['error_num'] = 0
    index_info_list = index_info.objects.all()
    response['index_info_list'] = json.loads(serializers.serialize("json", index_info_list))
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_index_analysis_info(request):
    response = {}
    indexAnalysis = index_analysis(request.GET['index_code'])
    resutl = indexAnalysis.get_index_analysis_info()
    if resutl == 'success':
        response['index_code'] = indexAnalysis.index_code
        response['last_analysis_date'] = indexAnalysis.last_analysis_date
        response['history_max_pe'] = indexAnalysis.history_max_pe
        response['history_min_pe'] = indexAnalysis.history_min_pe
        response['pe_ttm_now'] = indexAnalysis.pe_ttm_now
        response['pe_ttm_percentage'] = indexAnalysis.pe_ttm_percentage
        response['pe_ttm_percentage_5y'] = indexAnalysis.pe_ttm_percentage_5y
        response['pe_ttm_percentage_10y'] = indexAnalysis.pe_ttm_percentage_10y

        response['pb_ttm_now'] = indexAnalysis.pb_ttm_now
        response['pb_ttm_percentage'] = indexAnalysis.pb_ttm_percentage
        response['pb_ttm_percentage_5y'] = indexAnalysis.pb_ttm_percentage_5y
        response['pb_ttm_percentage_10y'] = indexAnalysis.pb_ttm_percentage_10y

        response['ps_ttm_now'] = indexAnalysis.ps_ttm_now
        response['ps_ttm_percentage'] = indexAnalysis.ps_ttm_percentage
        response['ps_ttm_percentage_5y'] = indexAnalysis.ps_ttm_percentage_5y
        response['ps_ttm_percentage_10y'] = indexAnalysis.ps_ttm_percentage_10y

        response['last_5day_data'] = indexAnalysis.last_5Day_data.to_json(orient="records", force_ascii=False)
        response['history_data'] = indexAnalysis.index_analysis_df.to_json(orient="records",force_ascii=False)
    else:
        response['msg'] = 'faild'
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def get_all_index_analysis_data(request):
    config_file_path = sys.path[0] + '\\index-analysis-data.json'
    config = open(config_file_path, encoding='utf-8')
    index_analysis_info = json.load(config)
    return JsonResponse(index_analysis_info)

@require_http_methods(["GET"])
def get_stocks_bonds_pe(request):
    response = {}

    # 获取10年期国债PE月末数据
    bond_df = bond_cn_service.get_bond_cn_10year_history_data()
    bond_df.set_index('trade_date', inplace=True)
    bond_df.index = pd.to_datetime(bond_df.index)
    bond_df.sort_index(inplace=True)
    bond_m = bond_df['pe_ttm'].resample('M').last()
    bond_m.rename(columns={"pe_ttm": "bond_pe_ttm"})

    # 获取全市场PE月末数据
    indexAnalysis = index_analysis('qzzs.sc')
    stocks_df = indexAnalysis.get_index_pe()
    stocks_df.set_index('trade_date', inplace=True)
    stocks_df.index = pd.to_datetime(stocks_df.index)
    stocks_df.sort_index(inplace=True)
    stocks_m = stocks_df['pe_ttm'].resample('M').last()
    stocks_m.rename(columns={"pe_ttm": "stocks_pe_ttm"})

    df = pd.DataFrame({'bond_pe':bond_m,'stocks_pe':stocks_m})
    print(df)

    df = df.reset_index()
    df['trade_date'] = df['trade_date'].astype(str)
    response['pe_history'] = df.to_json(orient="records",force_ascii=False)
    return JsonResponse(response)