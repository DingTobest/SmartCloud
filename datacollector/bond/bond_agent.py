
import pandas as pd
import json
import datetime
from datacollector.common import RestAgent
from bs4 import BeautifulSoup

class BondAgent(RestAgent):
    def __init__(self):
        RestAgent.__init__(self)
        self.add_headers({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0"})

    def get_china_10year_bond_yield_historical_data(self):
        url = "https://cn.investing.com/rates-bonds/china-10-year-bond-yield-historical-data"

        response = self.do_request(url)
        soup = BeautifulSoup(response, "html5lib")
        tables = soup.select("#curr_table")
        data_list = []

        for table in tables:
            if table.has_attr('id') and table['id'] == 'curr_table':
                trs = table.find('tbody').findAll("tr")
                for tr in trs:
                    tds = tr.findAll('td')
                    trade_date = datetime.datetime.fromtimestamp(int(tds[0]['data-real-value'])).strftime("%Y-%m-%d")
                    data_list.append({'trade_date': trade_date,
                                      'open': float(tds[2].text),
                                      'high': float(tds[3].text),
                                      'low': float(tds[4].text),
                                      'close': float(tds[1].text),
                                      })
        df = pd.DataFrame(data_list)
        return df, ''
