# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 07:35:59 2020

@author: mazhu
"""

import tushare as ts 
import numpy as np
import pandas as pd 

token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'

# setup tushare token        
ts.set_token(token)
ts_pro = ts.pro_api()
tick = '000001.SZ'


data_price  = ts.pro_bar(ts_code=tick, adj = 'hfq')


data_basic = ts_pro.daily_basic(ts_code=tick)

data_money_flow = ts_pro.moneyflow(ts_code=tick)




data_price['trade_date'] = pd.to_datetime(data_price['trade_date'])
data_price.set_index('trade_date',inplace=True)


data_basic['trade_date'] = pd.to_datetime(data_basic['trade_date'])
data_basic.set_index('trade_date', inplace = True)

data_money_flow['trade_date'] = pd.to_datetime(data_money_flow['trade_date'])
data_money_flow.set_index('trade_date', inplace = True)


test = data_money_flow.join(data_basic, how = 'inner')

pd.merge(data_money_flow,data_basic,how = 'inner')





import datetime
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
sns.set_style('white')

# daily capital flow data
engine_capital_flow = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow', encoding ='utf8')
sql_cmd = "SELECT * FROM `" + '000001.sz' + '`;'
daily_capital_flow = pd.read_sql(sql = sql_cmd, con = engine_capital_flow)

# daily basic
engine_daily = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic', encoding ='utf8')
sql_cmd = "SELECT * FROM `" + '000001.sz' + '`;'
daily_basic = pd.read_sql(sql = sql_cmd, con = engine_daily)

# daily price
engine_daily_price = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_price_daily', encoding ='utf8')
sql_cmd = "SELECT * FROM `" + '000001.sz_hfq' + '`;'
daily_price = pd.read_sql(sql = sql_cmd, con = engine_daily_price)



# reset index to time index
daily_capital_flow['trade_date'] = pd.to_datetime(daily_capital_flow['trade_date'])
daily_capital_flow.set_index('trade_date',inplace=True)
daily_capital_flow = daily_capital_flow[::-1]

daily_basic['trade_date'] = pd.to_datetime(daily_basic['trade_date'])
daily_basic.set_index('trade_date',inplace=True)
daily_basic = daily_basic[::-1]

daily_price['trade_date'] = pd.to_datetime(daily_price['trade_date'])
daily_price.set_index('trade_date',inplace=True)
daily_price = daily_price[::-1]

data_merge_1 = pd.merge(daily_capital_flow,daily_price,left_index = True, right_index = True)
del data_merge_1['ts_code_y']
data_merge_2 = pd.merge(data_merge_1,daily_basic,left_index = True, right_index = True)
del data_merge_2['ts_code_x']
del data_merge_2['close_x']
data_merge_2 = data_merge_2.rename(columns = {'close_y' : 'close'})

data_merge_2 = data_merge_2.dropna()



label = []

inc_pct = 0.1
dec_pct = 0.05
period = 5

for i in range(len(data_merge_2)-5):
    date_price = data_merge_2.iloc[i]['close']
    target_price = [date_price * (1 - dec_pct ), date_price * (1 + inc_pct)]
    
    flag = False
    
    for j in range(1,6):
        if data_merge_2.iloc[i + j]['low'] <= target_price[0]:
            print(i)
            label.append(0)
            flag = True
            break
        elif data_merge_2.iloc[i + j]['high'] >= target_price[1]:
            label.append(1)
            flag = True
            break
    
    if flag:
        continue
        
    period_ret = data_merge_2.iloc[i + j]['close'] / date_price - 1
    label.append(period_ret)


placeholder = [np.nan] * period
label = label + placeholder
data_merge_2['label'] = label
        


































