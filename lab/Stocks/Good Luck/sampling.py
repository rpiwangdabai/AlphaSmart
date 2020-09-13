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

# # daily price
# engine_daily_price = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily', encoding ='utf8')
# sql_cmd = "SELECT * FROM `" + '000001.sz_hfq' + '`;'
# daily_price = pd.read_sql(sql = sql_cmd, con = engine_daily_price)


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


del daily_basic['ts_code']
del daily_price['ts_code']
data_merge_1 = daily_capital_flow.join(daily_basic)
data_merge_2 = data_merge_1.join(daily_price, lsuffix='_daily_close_price')
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

data_merge_2 = data_merge_2.dropna()
        

'''-----------------------------------------'''
a = pd.DataFrame()
a['columns'] = list(data_merge_2.columns)

data_derivative_variables = pd.DataFrame(index = data_merge_2.index)

set_one_variables = list(data_merge_2.columns)[1:19]


'''----original variable proportion----'''

sub_dataset = data_merge_2[set_one_variables[:16]]

data_vol = sub_dataset.iloc[:, [i%2 == 0 for i in range(len(set_one_variables[:16]))]]
data_amount = sub_dataset.iloc[:, [i%2 == 1 for i in range(len(set_one_variables[:16]))]]

data_vol_proportion = data_vol.div(data_vol.sum(axis=1), axis=0)
data_amount_proportion = data_amount.div(data_amount.sum(axis=1), axis=0)

'''---columns_rename---'''
col_ratio = []
for col in data_vol_proportion.columns:
    col_ratio.append(col + '_ratio')

data_vol_proportion.columns = col_ratio

col_ratio = []
for col in data_amount_proportion.columns:
    col_ratio.append(col + '_ratio')

data_amount_proportion.columns = col_ratio

data_proportion = data_amount_proportion.join(data_vol_proportion)


'''----Z value variables----'''

for column in set_one_variables:
    
    column_name = column + '_z_value'
    
    data_derivative_variables[column_name] = (data_merge_2[column] - data_merge_2[column].rolling(window = 5).median()) / data_merge_2[column].rolling(window = 5).std()



for column in data_proportion.columns:
    
    column_name = column + '_z_value'
    
    data_derivative_variables[column_name] = (data_proportion[column] - data_proportion[column].rolling(window = 5).median()) / data_proportion[column].rolling(window = 5).std()





data_derivative_variables = data_derivative_variables.join(data_proportion)











