# -*- coding: utf-8 -*-
# @Time    : 2020-03-21 11:55
# @Author  : Dingzh.tobest
# 文件描述  ： jenkins定时任务驱动程序
#             调用接口，并形成html文件，用于返回每日计算数据

import requests
import json
import os

import sys

host_address = 'http://127.0.0.1:8000'

html_template = """
<tr>
    <td>%s</td>
    <td>%s</td>
    <td>%.2f</td>
    <td>%.2f</td>
    <td>%.2f</td>
    <td>%s</td>
	<td>%s</td>
    <td>%s</td>
	<td>%.2f</td>
    <td>%s</td>
	<td>%s</td>
    <td>%s</td>
	<td>%.2f</td>
    <td>%s</td>
	<td>%s</td>
    <td>%s</td>
</tr>"""

COLOR_VERY_LOW = '#00FF00'
COLOR_LOW = '#F0E68C'
COLOR_HIGH = '#87CEEB'
COLOR_VERY_HIGH = '#FF4500'

# 调用每日计算函数
def call_calc_index_analysis_info():
    addr = host_address + '/timingtask/calc_index_analysis_info'
    r = requests.post(addr)
    if r.status_code == 200:
        resutl = json.loads(r.text)
        print(resutl['result'])
    else:
        raise Exception('更新每日数据接口【call_calc_index_analysis_info】调用失败')

def get_color(ttm_5y, ttm_10y, ttm_history):
    ttm_now_color = ''
    ttm_percentage_10y_color = ''
    ttm_percentage_history_color = ''
    if ttm_10y != '' and float(ttm_10y[:-1]) > 60:
        if float(ttm_10y[:-1]) > 90:
            color_str = COLOR_VERY_HIGH
        else:
            color_str = COLOR_HIGH
        ttm_percentage_10y_color = color_str
        ttm_now_color = color_str
    elif ttm_10y != '' and float(ttm_10y[:-1]) < 30:
        if float(ttm_10y[:-1]) < 10:
            color_str = COLOR_VERY_LOW
        else:
            color_str = COLOR_LOW
        ttm_percentage_10y_color = color_str
        ttm_now_color = color_str
    elif ttm_history != '' and ttm_5y != '' and ttm_10y == '' and float(
            ttm_history[:-1]) > 60:
        if float(ttm_history[:-1]) > 90:
            color_str = COLOR_VERY_HIGH
        else:
            color_str = COLOR_HIGH
        ttm_percentage_history_color = color_str
        ttm_now_color = color_str
    elif ttm_history != '' and ttm_5y != '' and ttm_10y == '' and float(
            ttm_history[:-1]) < 30:
        if float(ttm_history[:-1]) < 10:
            color_str = COLOR_VERY_LOW
        else:
            color_str = COLOR_LOW
        ttm_percentage_history_color = color_str
        ttm_now_color = color_str

    return ttm_now_color, ttm_percentage_10y_color, ttm_percentage_history_color

# 调用全部指数的计算结果，生成html结果文件
def call_index_analysis_info_result():
    addr = host_address + '/stock/get_stock_info'
    r = requests.get(addr)
    if r.status_code == 200:
        resutl = json.loads(r.text)

        html = ""

        # 用于存储转化后的数据对象
        last_update_date = ""
        index_analysis_list = []

        for index_info in resutl['index_info_list']:
            index_info_dict = {}
            info = index_info['fields']

            # 拼装返回html的字段
            index_name = info['index_name']
            start_date = info['start_date']
            print('正在获取数据的指数：' + index_name)

            # 获取数据的请求参数
            aparam = {'index_code': info['index_data_table']}
            addr_analysis = host_address + '/stock/get_index_analysis_info'
            ar = requests.get(addr_analysis, params=aparam)
            if ar.status_code != 200:
                raise Exception('获取指数信息【get_index_analysis_info】调用失败：' + info['index_data_table'])

            analysis_info = json.loads(ar.text)
            history_max_pe = analysis_info['history_max_pe']
            history_min_pe = analysis_info['history_min_pe']
            pe_ttm_now = analysis_info['pe_ttm_now']
            pe_ttm_percentage = analysis_info['pe_ttm_percentage']
            pe_ttm_percentage_5y = analysis_info['pe_ttm_percentage_5y']
            pe_ttm_percentage_10y = analysis_info['pe_ttm_percentage_10y']

            pe_ttm_now_color, pe_ttm_percentage_10y_color, pe_ttm_percentage_color = get_color(pe_ttm_percentage_5y, pe_ttm_percentage_10y, pe_ttm_percentage)

            last_update_date = analysis_info['last_analysis_date']

            pb_ttm_now = analysis_info['pb_ttm_now']
            pb_ttm_percentage = analysis_info['pb_ttm_percentage']
            pb_ttm_percentage_5y = analysis_info['pb_ttm_percentage_5y']
            pb_ttm_percentage_10y = analysis_info['pb_ttm_percentage_10y']

            pb_ttm_now_color, pb_ttm_percentage_10y_color, pb_ttm_percentage_color = get_color(pb_ttm_percentage_5y, pb_ttm_percentage_10y, pb_ttm_percentage)

            ps_ttm_now = analysis_info['ps_ttm_now']
            ps_ttm_percentage = analysis_info['ps_ttm_percentage']
            ps_ttm_percentage_5y = analysis_info['ps_ttm_percentage_5y']
            ps_ttm_percentage_10y = analysis_info['ps_ttm_percentage_10y']

            # 用于生成数据存储的json数据
            index_info_dict['index_code'] = info['index_code']
            index_info_dict['index_data_table'] = info['index_data_table']
            index_info_dict['index_name'] = index_name
            index_info_dict['start_date'] = start_date

            index_info_dict['history_max_pe'] = history_max_pe
            index_info_dict['history_min_pe'] = history_min_pe
            index_info_dict['pe_ttm_now'] = pe_ttm_now
            index_info_dict['pe_ttm_percentage'] = pe_ttm_percentage
            index_info_dict['pe_ttm_percentage_5y'] = pe_ttm_percentage_5y
            index_info_dict['pe_ttm_percentage_10y'] = pe_ttm_percentage_10y

            index_info_dict['pb_ttm_now'] = pb_ttm_now
            index_info_dict['pb_ttm_percentage'] = pb_ttm_percentage
            index_info_dict['pb_ttm_percentage_5y'] = pb_ttm_percentage_5y
            index_info_dict['pb_ttm_percentage_10y'] = pb_ttm_percentage_10y

            index_info_dict['ps_ttm_now'] = ps_ttm_now
            index_info_dict['ps_ttm_percentage'] = ps_ttm_percentage
            index_info_dict['ps_ttm_percentage_5y'] = ps_ttm_percentage_5y
            index_info_dict['ps_ttm_percentage_10y'] = ps_ttm_percentage_10y

            index_analysis_list.append(index_info_dict)


            # 用于生成邮件返回的html信息
            temp_html = "<tr>"
            temp_html += "<td>%s</td>" % index_name
            temp_html += "<td>%s</td>" % start_date
            temp_html += "<td>%.2f</td>" % history_max_pe
            temp_html += "<td>%.2f</td>" % history_min_pe
            if pe_ttm_now_color == '':
                temp_html += "<td>%.2f</td>" % pe_ttm_now
            else:
                temp_html += "<td bgcolor=\"%s\">%.2f</td>" % (pe_ttm_now_color, pe_ttm_now)
            temp_html += "<td>%s</td>" % pe_ttm_percentage_5y
            if pe_ttm_percentage_10y_color == '':
                temp_html += "<td>%s</td>" % pe_ttm_percentage_10y
            else:
                temp_html += "<td bgcolor=\"%s\">%s</td>" % (pe_ttm_percentage_10y_color, pe_ttm_percentage_10y)
            if pe_ttm_percentage_color == '':
                temp_html += "<td>%s</td>" % pe_ttm_percentage
            else:
                temp_html += "<td bgcolor=\"%s\">%s</td>" % (pe_ttm_percentage_color, pe_ttm_percentage)

            if pb_ttm_now_color == '':
                temp_html += "<td>%.2f</td>" % pb_ttm_now
            else:
                temp_html += "<td bgcolor=\"%s\">%.2f</td>" % (pb_ttm_now_color, pb_ttm_now)
            temp_html += "<td>%s</td>" % pb_ttm_percentage_5y
            if pb_ttm_percentage_10y_color == '':
                temp_html += "<td>%s</td>" % pb_ttm_percentage_10y
            else:
                temp_html += "<td bgcolor=\"%s\">%s</td>" % (pb_ttm_percentage_10y_color, pb_ttm_percentage_10y)
            if pb_ttm_percentage_color == '':
                temp_html += "<td>%s</td>" % pb_ttm_percentage
            else:
                temp_html += "<td bgcolor=\"%s\">%s</td>" % (pb_ttm_percentage_color, pb_ttm_percentage)

            temp_html += "<td>%.2f</td>" % ps_ttm_now
            temp_html += "<td>%s</td>" % ps_ttm_percentage_5y
            temp_html += "<td>%s</td>" % ps_ttm_percentage_10y
            temp_html += "<td>%s</td>" % ps_ttm_percentage
            temp_html += "</tr>"

            html += temp_html

        # 生成数据存储的json文件
        index_data_dict = {'last_update_date': last_update_date, 'index_analysis_list' : index_analysis_list}
        # index_analysis_json = json.dumps(index_data_dict, ensure_ascii=False)
        json_file_path = sys.path[0] + '\\index-analysis-data.json'
        print(json_file_path)
        if os.path.exists(json_file_path):
            os.remove(json_file_path)
            print('删除历史文件index-analysis-data.json')

        with open(json_file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(index_data_dict, ensure_ascii=False, indent=4))

        # 生成邮件发送的html文件
        print(html)
        print(sys.path[0] + '\\email-template.html')
        f = open(sys.path[0] + '\\email-template.html', 'r', encoding='utf-8')
        html_temp = f.read()
        f.close()
        email_html = html_temp.replace('#$%index_analysis_info#$%', html)

        if os.path.exists(sys.path[0] + '\\email-html-utf8.html'):
            os.remove(sys.path[0] + '\\email-html-utf8.html')
            print('删除历史文件email-html-utf8.html')

        f2 = open(sys.path[0] + '\\email-html-utf8.html', 'w', encoding='utf-8')
        f2.write(email_html)
        f2.close()

        if os.path.exists(sys.path[0] + '\\email-html.html'):
            os.remove(sys.path[0] + '\\email-html.html')
            print('删除历史文件email-html.html')

        temp_email_html = email_html
        f3 = open(sys.path[0] + '\\email-html.html', 'w', encoding='gb18030')
        gbk_email_html = str(temp_email_html.encode('gbk'), encoding="gbk")
        f3.write(gbk_email_html)
        f3.close()

        print('生成用于返回email的html文件成功！')
    else:
        raise Exception('获取指数信息【get_stock_info】调用失败')

if __name__ == '__main__':
    call_calc_index_analysis_info()
    call_index_analysis_info_result()