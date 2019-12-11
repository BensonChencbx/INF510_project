

# step 1 -- find 2 funds and compare the time of begining of them to choose the short one as the period

# 1.1 active management fund (GS -- Goldman Sachs Group Inc. (The))
import Active_Fund
active_fund = Active_Fund.ActiveFund('GS')
active_time = active_fund.fund

# 1.2 passive management fund (ONEQ -- Fidelity NASDAQ Composite Index Tracking Stock Fund)
import Passive_Fund
passive_fund = Passive_Fund.PassiveFund('ONEQ')
passive_time = passive_fund.fund

# 1.3 compare which one is the earlier one
import Algorithm
result_time = Algorithm.compare(active_time, passive_time)

# step 2 -- extract the close price of 2 funds and treasury bond rate in that period

# 2.1 extract the close price of active management fund
active_frame = active_fund.extract(result_time)
print(active_frame)

# 2.2 extract the close price of passive management fund
passive_frame = passive_fund.extract(result_time)
print(passive_frame)

# 2.3 extract the daily curve rate of treasury bond 
import Treasury_Bill
treasury_bill = Treasury_Bill. TreasuryBill()
treasury_frame = treasury_bill.extract(result_time)
print(treasury_frame)

# step 3 -- set the weight mechanism to adjust the weights of 3 assets every 5 days according to their return

# 3.1 compare which frame has the longest column and combine the two frames of funds

frame = Algorithm.combine(active_frame, passive_frame, treasury_frame)
print(frame)

# 3.2 value series = weight * 3 seperate growth rate in every 5 days 
import numpy as np
price1 = np.array(frame['Price'])
price2 = np.array(frame['New_Price'])
bill_rate = np.array(frame['Treasury_Rate'])
price1 = price1.tolist()
price2 = price2.tolist()
bill_rate = bill_rate.tolist()

interest_rate1 = []
for i in range(0, len(price1), 5):
    count = i + 5
    if i == 0:
        continue
    if count > len(price1):
        rate = round((price1[-1] - price1[i])/price1[i], 5)
    else:
        rate = round((price1[i] - price1[i-5])/price1[i-5], 5)
    interest_rate1.append(rate)

price2 = Algorithm.update(price2)
interest_rate2 = []
for i in range(0, len(price2), 5):
    i = int(i)
    count = i + 5
    if i == 0:
        continue
    if count > len(price2):
        rate = round((price2[-1] - price2[i])/price2[i], 5)
    else:
        rate = round((price2[i] - price2[i-5])/price2[i-5], 5)
    interest_rate2.append(rate)

bill_rate = Algorithm.update(bill_rate)
interest_rate3 = []
for i in range(0, len(bill_rate), 5):
    i = int(i)
    count = i + 5
    if i == 0:
        continue
    if count > len(bill_rate):
        if bill_rate[i] == 'NA':
            rate = interest_rate3[-1]
        rate = round(((bill_rate[-1] - bill_rate[i])*4 *5)/365, 5)
    else:
        if bill_rate[i] == 'NA':
            rate = interest_rate3[-1]
        rate = round(((bill_rate[i] - bill_rate[i-5])*4 *5)/365, 5)
    interest_rate3.append(rate)

together = []
for i in range(0, len(interest_rate1)):
    add_them = round(interest_rate1[i] + interest_rate2[i] + interest_rate3[i], 5)
    together.append(add_them)

rate1 = np.array(interest_rate1)
rate2 = np.array(interest_rate2)
rate3 = np.array(interest_rate3)
together = np.array(together)

weight1, weight2, weight3 = Algorithm.weight(interest_rate1, interest_rate2, interest_rate3, together)
weight1 = np.array(weight1)
weight2 = np.array(weight2)
weight3 = np.array(weight3)

period1st = 1/3
weight1 = np.insert(weight1, 0, period1st)
weight2 = np.insert(weight2, 0, period1st)
weight3 = np.insert(weight3, 0, period1st)
weight1 = np.delete(weight1, -1)
weight2 = np.delete(weight2, -1)
weight3 = np.delete(weight3, -1)

# step 4 -- get the return and performance of portfolio and compare with each component seperatly

# 4.1 the rate of return in whole investment
total_interest_rate = rate1 * weight1 + rate2 * weight2 + rate3 * weight3
base = np.ones_like(total_interest_rate)
total_rate = total_interest_rate + base
result = 1
for i in total_rate:
    result *= i

# 4.2 calculate the standard deviation of the portfolio and seperate asset to indicate 
# Sharp Ratio and compare the performance individually
import datetime
this_year = datetime.date.today().year
period = (float(this_year) - float(result_time[0]))
import pandas as pd
total_rate = pd.DataFrame(total_interest_rate)
describe = total_rate.describe()
mean = describe.iloc[1][0]
standard_deviation = describe.iloc[2][0]
portfolio_sharp = (float(result - 1)/period - float(mean)) / float(standard_deviation)
result = round(result, 4)
portfolio_sharp = round(portfolio_sharp, 4)
print(f'The return of portfolio is {result} and the excess return per risk share is {portfolio_sharp}')

base = np.ones_like(rate1)
total_rate = rate1 + base
result1 = 1
for i in total_rate:
    result1 *= i
rate1_frame = pd.DataFrame(rate1)
describe = rate1_frame.describe()
mean = describe.iloc[1][0]
standard_deviation = describe.iloc[2][0]
active_sharp = (float(result1 - 1)/period - float(mean)) / float(standard_deviation)
result1 = round(result1, 4)
active_sharp = round(active_sharp, 4)
print(f'The return of active fund is {result1} and the excess return per risk share is {active_sharp}')

base = np.ones_like(rate2)
total_rate = rate2 + base
result2 = 1
for i in total_rate:
    result2 *= i
rate2_frame = pd.DataFrame(rate2)
describe = rate2_frame.describe()
mean = describe.iloc[1][0]
standard_deviation = describe.iloc[2][0]
passive_sharp = (float(result2 - 1)/period - float(mean)) / float(standard_deviation)
result2 = round(result2, 4)
passive_sharp = round(passive_sharp, 4)
print(f'The return of passive fund is {result2} and the excess return per risk share is {passive_sharp}')

base = np.ones_like(rate3)
total_rate = rate3 + base
result3 = 1
for i in total_rate:
    result3 *= i
rate3_frame = pd.DataFrame(rate3)
describe = rate3_frame.describe()
mean = describe.iloc[1][0]
standard_deviation = describe.iloc[2][0]
treasury_sharp = (float(result3 - 1)/period - float(mean)) / float(standard_deviation)
result3 = round(result3, 4)
treasury_sharp = round(treasury_sharp, 4)
print(f'The return of treasury bill is {result3} and the excess return per risk share is {treasury_sharp}')

# step 5 -- store the result into txt file and csv file
import os
os.getcwd()
with open('Result_txt.txt', 'w') as t:
    t.write("1. What are the strengths of your data modeling format?"+'\n'+"It can obtain the rerurn and the performance of any two funds you choose as long as you have their abbreviations of the name. You will get a form which contians the return and performance of the portfolio (two funds and 3-months treasury of U.S.) and each asset seperately to compare which one performs better on U.S.'s capital market."+'\n\n')
    t.write("2. What are the weaknesses?  (Does your data model support?  Sorting the information? Re-ordering it? Only obtaining a certain subset of the information?) "+'\n'+"My model use the close price and rate of the former day to replace the non-available value so I think it might cause some small inaccuracy of my result. Also, my model ignores the trading cost and time cost, which means that the model assumes you can buy and sell the asset at the price you see immediately, but actually that's impossible and you might have some loss in the trading process."+'\n\n')
    t.write("3. How do you store your data on disk? "+'\n'+"I store them as a .txt file in the end as well as .csv file in the zip file."+'\n\n')
    t.write("4. Let’s say you find another data source that relates to all 3 of your data sources (i.e. a data source that relates to your existing data).  How would you extend your model to include this new data source?  How would that change the interface?"+'\n'+"My model can obtain any fund on the capital market when you input different abbreviation of their names at the begining of the code. It will find the shorter one of the fund period between two funds and use this shorter time to scrape the 3-months U.S. treasury rate from website at the same period. Then the model will calculate their performance and total return of whole portfolio as well as each asset. I think I will modify the begining part to add an input function to fit my idea properly."+'\n\n')
    t.write("5. How would you add a new attribute to your data (i.e. imagine you had a lat/long column in a database.  You might use that to access an API to get a city name.  How would you add city name to your data?) "+'\n'+"First, I should extract the lat/long column from my database and add them to the request by changing the code of accessing an API. Then, I should get the returned information into the new blank column at my database"+'\n\n\n\n')
    
    t.write(f'The time period is calculated as the shorter one of the two funds which is {period} years'+'\n\n')
    t.write('Then we scraped the 3-months treasury bill from the website according to the period'+'\n\n')
    t.write('Then we get the 3 frames of three assets and the total frame of them and save them in Result_excel file in the end'+'\n\n')
    t.write('Then we could calculate the return rates seperately and calculate the weight of investing them according to their performance every 5 days and save these data in Result_csv file'+'\n\n')
    t.write('Finally, we can get the result of their return among the period and calculate the excess return per risk share each year'+'\n\n')
    t.write('That means the final multiple of your capital has gained and the multiple your capital has gained each year if you invest this asset in the begining'+'\n\n')
    t.write(f'The return of portfolio is {result} and the excess return per risk share each year is {portfolio_sharp}'+'\n')
    t.write(f'The return of active fund is {result1} and the excess return per risk share each year is {active_sharp}'+'\n')
    t.write(f'The return of passive fund is {result2} and the excess return per risk share each year is {passive_sharp}'+'\n')
    t.write(f'The return of treasury bill is {result3} and the excess return per risk share each year is {treasury_sharp}'+'\n')
    t.close()

writer = pd.ExcelWriter('Result_excel.xlsx', engine='xlsxwriter')

active_frame.to_excel(writer, sheet_name='Active_Frame')
passive_frame.to_excel(writer, sheet_name='Passive_Frame')
treasury_frame.to_excel(writer, sheet_name='Treasury_Frame')
frame.to_excel(writer, sheet_name='Total_Frame')

rate1 = pd.DataFrame(rate1)
rate2 = pd.DataFrame(rate2)
rate3 = pd.DataFrame(rate3)
weight1 = pd.DataFrame(weight1)
weight2 = pd.DataFrame(weight2)
weight3 = pd.DataFrame(weight3)
rate_weight = pd.concat([rate1,rate2, rate3, weight1, weight2, weight3], axis=1)
rate_weight.columns = ['rate1', 'rate2', 'rate3', 'weight1', 'weight2', 'weight3']
rate_weight.to_excel(writer, sheet_name='Rate_Weight')

writer.save()