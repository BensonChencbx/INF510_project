'''
You can choose any passive fund as long as you have its symbol
In this case, I chose "Fidelity Nasdaq Composite Index Tracking Stock" as an example, which symbol is "ONEQ"
'''
# 1.2 get the begining time of a passive management fund (ONEQ -- Fidelity NASDAQ Composite Index Tracking Stock Fund)
from urllib.request import urlopen
import json
import pandas as pd

class PassiveFund:
    def __init__(self, id):
        self.id = id
        self.url = ("https://financialmodelingprep.com/api/v3/historical-price-full/"+ self.id +"?serietype=line") 
        self.response = urlopen(self.url)
        self.data = self.response.read().decode("utf-8")
        self.total = json.loads(self.data)
        self.time = self.total['historical'][0]['date']
        self.fund = self.time.split('-')
        
    # 2.2 extract the close price of passive management fund
    def extract(self, begin_time):
        data = self.total['historical']
        passive_close = {}
        begin_year = int(begin_time[0])
        begin_month = int(begin_time[1])
        begin_day = int(begin_time[2])
        for each in data:
            year = each['date'].split('-')[0]
            month = each['date'].split('-')[1]
            day = each['date'].split('-')[2]
            if int(year) > begin_year:
                passive_close[each['date']] = each['close']
            else:
                if int(year) == begin_year:
                    if int(month) > begin_month:
                        passive_close[each['date']] = each['close']
                    else:
                        if int(month) == begin_month:
                            if int(day) >= begin_day:
                                passive_close[each['date']] = each['close']
        passive_close = pd.DataFrame({'Date':list(passive_close.keys()), 'Price':list(passive_close.values())})
        return passive_close
