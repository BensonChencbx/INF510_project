'''
You can choose any active fund as long as you have its symbol
In this case, I chose "Goldman Sachs Group Inc. (The)" as an example, which symbol is "GS"
'''
# 1.1 get the begining time of an active management fund (GS -- Goldman Sachs Group Inc. (The))
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

class ActiveFund:
    def __init__(self, id):
        self.id = id
        key = 'YNER5OQ3FMOTFGFM'
        ts = TimeSeries(key)
        self.total = ts.get_daily(self.id, outputsize='full')[0]
        self.time = list(self.total.keys())[-1]
        self.fund = self.time.split('-')

# 2.1 extract the close price of active management fund
    def extract(self, begin_time):
        active_close = {}
        begin_year = int(begin_time[0])
        begin_month = int(begin_time[1])
        begin_day = int(begin_time[2])
        for year in range(begin_year, 2020):
            year = str(year)
            if int(year) == begin_year:
                for month in range(begin_month, 12):
                    if month < 10:
                        month = str(0)+str(month)
                    else:
                        month = str(month)
                    if int(month) == begin_month:
                        for day in range(begin_day, 31):
                            if day < 10:
                                day = str(0)+str(day)
                            else:
                                day = str(day)
                            time = year+'-'+month+'-'+day
                            if time in list(self.total.keys()):
                                value = self.total[time]['4. close']
                                active_close[time] = float(value)
                    else:
                        for day in range(1, 31):
                            if day < 10:
                                day = str(0)+str(day)
                            else:
                                day = str(day)
                            time = year+'-'+month+'-'+day
                            if time in list(self.total.keys()):
                                value = self.total[time]['4. close']
                                active_close[time] = float(value)
            else:
                for month in range(1, 12):
                    if month < 10:
                        month = str(0)+str(month)
                    else:
                        month = str(month)
                    for day in range(1, 31):
                        if day < 10:
                            day = str(0)+str(day)
                        else:
                            day = str(day)
                        time = year+'-'+month+'-'+day
                        if time in list(self.total.keys()):
                            value = self.total[time]['4. close']
                            active_close[time] = float(value)
        active_close = pd.DataFrame({'Date':list(active_close.keys()), 'Price':list(active_close.values())})
        return active_close