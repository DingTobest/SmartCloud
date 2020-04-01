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

# 调用每日计算函数
def call_calc_index_analysis_info():
    addr = host_address + '/timingtask/calc_index_analysis_info'
    r = requests.get(addr)
    if r.status_code == 200:
        resutl = json.loads(r.text)
        print(resutl['result'])
    else:
        raise Exception('更新每日数据接口【call_calc_index_analysis_info】调用失败')

# 调用全部指数的计算结果，生成html结果文件
def call_index_analysis_info_result():
    addr = host_address + '/stock/get_stock_info'
    r = requests.get(addr)
    if r.status_code == 200:
        resutl = json.loads(r.text)

        html = ""

        for index_info in resutl['index_info_list']:
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

            pe_ttm_now_color = ''
            pe_ttm_percentage_10y_color = ''
            pb_ttm_percentage_color = ''
            if pe_ttm_percentage_10y != '' and float(pe_ttm_percentage_10y[:-1]) > 60:
                if float(pe_ttm_percentage_10y[:-1]) > 90:
                    color_str = '#FFCC00'
                else:
                    color_str = '#87CEEB'
                pe_ttm_percentage_10y_color = color_str
                pe_ttm_now_color = color_str
            elif pe_ttm_percentage_10y != '' and float(pe_ttm_percentage_10y[:-1]) < 30:
                if float(pe_ttm_percentage_10y[:-1]) < 10:
                    color_str = '#00FF00'
                else:
                    color_str = '#F0E68C'
                pe_ttm_percentage_10y_color = color_str
                pe_ttm_now_color = color_str
            elif pe_ttm_percentage != '' and float(pe_ttm_percentage[:-1]) > 60:
                if float(pe_ttm_percentage[:-1]) > 90:
                    color_str = '#FFCC00'
                else:
                    color_str = '#87CEEB'
                pb_ttm_percentage_color = color_str
                pe_ttm_now_color = color_str
            elif pe_ttm_percentage != '' and float(pe_ttm_percentage[:-1]) < 30:
                if float(pe_ttm_percentage[:-1]) < 10:
                    color_str = '#00FF00'
                else:
                    color_str = '#F0E68C'
                pb_ttm_percentage_color = color_str
                pe_ttm_now_color = color_str

            pb_ttm_now = analysis_info['pb_ttm_now']
            pb_ttm_percentage = analysis_info['pb_ttm_percentage']
            pb_ttm_percentage_5y = analysis_info['pb_ttm_percentage_5y']
            pb_ttm_percentage_10y = analysis_info['pb_ttm_percentage_10y']

            ps_ttm_now = analysis_info['ps_ttm_now']
            ps_ttm_percentage = analysis_info['ps_ttm_percentage']
            ps_ttm_percentage_5y = analysis_info['ps_ttm_percentage_5y']
            ps_ttm_percentage_10y = analysis_info['ps_ttm_percentage_10y']

            # html += html_template % (index_name, start_date, history_max_pe, history_min_pe, pe_ttm_now, pe_ttm_percentage_5y, pe_ttm_percentage_10y, pe_ttm_percentage, pb_ttm_now, pb_ttm_percentage_5y, pb_ttm_percentage_10y, pb_ttm_percentage, ps_ttm_now, ps_ttm_percentage_5y, ps_ttm_percentage_10y, ps_ttm_percentage)

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
            if pb_ttm_percentage_color == '':
                temp_html += "<td>%s</td>" % pe_ttm_percentage
            else:
                temp_html += "<td bgcolor=\"%s\">%s</td>" % (pb_ttm_percentage_color, pe_ttm_percentage)
            temp_html += "<td>%.2f</td>" % pb_ttm_now
            temp_html += "<td>%s</td>" % pb_ttm_percentage_5y
            temp_html += "<td>%s</td>" % pb_ttm_percentage_10y
            temp_html += "<td>%s</td>" % pb_ttm_percentage
            temp_html += "<td>%.2f</td>" % ps_ttm_now
            temp_html += "<td>%s</td>" % ps_ttm_percentage_5y
            temp_html += "<td>%s</td>" % ps_ttm_percentage_10y
            temp_html += "<td>%s</td>" % ps_ttm_percentage
            temp_html += "</tr>"

            html += temp_html

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