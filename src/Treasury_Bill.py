'''
The period of treasury was chosen according to the time period of two funds since the period of 
treasury of United States must be longer than the period of two funds.
'''
# 2.3 extract the daily curve rate of treasury bond 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

class TreasuryBill:
    def __init__(self, name=None):
        self.name = name
    
    def one_year(self, year):
        r = requests.get("https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year="+str(year), timeout=30)
        soup = BeautifulSoup(r.content, 'lxml')
        bond_rate = {}
        main_table = soup.find_all('table', {"class" : "t-chart"})[0]
        main_body1 = main_table.find_all('tr',{'class':'oddrow'})
        main_body2 = main_table.find_all('tr',{'class':'evenrow'})
        for i in range(0, len(main_body1)):
            time = main_body1[i].find_all('td')[0].text
            rate = main_body1[i].find_all('td')[3].text
            time = time.split('/')
            time = '20'+ time[2] + '-' + time[0] + '-' + time[1]
            try:
                rate = float(rate)
            except:
                rate = main_body1[i-1].find_all('td')[3].text   
            bond_rate[time] = rate
            try:
                main_body2[i]
            except:
                pass
            else:
                time = main_body2[i].find_all('td')[0].text
                rate = main_body2[i].find_all('td')[3].text
                time = time.split('/')
                time = '20'+ time[2] + '-' + time[0] + '-' + time[1]
                try:
                    rate = float(rate)
                except:
                    rate = main_body2[i-1].find_all('td')[3].text   
                bond_rate[time] = rate
        return bond_rate
    
    def extract(self, begin_time):
        bill_rate = {}
        begin_year = int(begin_time[0])
        count_year = begin_year
        begin_month = int(begin_time[1])
        begin_day = int(begin_time[2])
        this_year = datetime.date.today().year
        while True:
            if count_year == this_year + 1:
                break
            final = self.one_year(count_year)
            for each in final.items():
                year = each[0].split('-')[0]
                month = each[0].split('-')[1]
                day = each[0].split('-')[2]
                if int(year) > begin_year:
                    bill_rate[each[0]] = each[1]
                elif int(year) == begin_year:
                    if int(month) > begin_month:
                        bill_rate[each[0]] = each[1]
                    elif int(month) == begin_month:
                        if int(day) >= begin_day:
                            bill_rate[each[0]] = each[1] 
            count_year += 1
        bill_rate = pd.DataFrame({'Date':list(bill_rate.keys()), 'Rate':list(bill_rate.values())})
        return bill_rate
