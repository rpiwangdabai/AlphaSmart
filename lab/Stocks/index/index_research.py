#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:26:17 2020

@author: Roy
"""

import tushare as ts 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import deque
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

'''----------get all stocks' ticks----------'''

token = '260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c'
ts.set_token(token)

ts_pro = ts.pro_api()

data_l = ts_pro.stock_basic(exchange='', list_status='L')

data_l.to_csv('/Users/Roy/Documents/Investment/Investment_lab/Stocks/index/stock_ticks.csv',
              index = False)

# data_d = ts_pro.stock_basic(exchange='', list_status='D') # 退市

# data_p = ts_pro.stock_basic(exchange='', list_status='P')

'''----------analysis----------'''

for i in range(2005,2020):
    print('running stock ipo in %d' %i)


    start_time = str(i) + '0101'
    end_time = str(i + 1) + '0101'
    
    sorted_data = data_l[(data_l.list_date > start_time) & (data_l.list_date < end_time)].sort_values('list_date')
    
    # sorted_data = data_l[(data_l.list_date < start_time)].sort_values('list_date')
    
    stock_ticks = deque(sorted_data['ts_code'])
    
    initial_date = sorted_data.list_date.iloc[0]
    end_date = '20200608'
    
    total_mv_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
    cric_mv_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
    # get data and merge
    # create engine
    engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks', 
                         encoding ='utf8')
    
    
    
    while stock_ticks:
        # get tick and date
        tick = stock_ticks.popleft()
        sql_cmd = "SELECT * FROM `" + tick + '`;'
        stock_data = pd.read_sql(sql=sql_cmd, con=engine)
        # set trade date as index
        stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date'])
        stock_data.set_index('trade_date', inplace = True)
        # select columns
        selected_data_total_mv = pd.DataFrame(stock_data['total_mv'])
        selected_data_circ_mv = pd.DataFrame(stock_data['circ_mv'])
        # merge 
        total_mv_merge_by_date['total_mv_' + tick] = selected_data_total_mv
        cric_mv_merge_by_date['circ_mv_' + tick] = selected_data_circ_mv
    
    #  delete hoilday 
    total_mv_merge_by_date = total_mv_merge_by_date.dropna(how = 'all')
    cric_mv_merge_by_date = cric_mv_merge_by_date.dropna(how = 'all')
    # fill na with fill
    total_mv_merge_by_date = total_mv_merge_by_date.fillna(method = 'ffill', axis = 0)
    cric_mv_merge_by_date = cric_mv_merge_by_date.fillna(method = 'ffill', axis = 0)
    # fill initial zero value with 0
    total_mv_merge_by_date = total_mv_merge_by_date.fillna(0)
    cric_mv_merge_by_date = cric_mv_merge_by_date.fillna(0)
    # calcualte weighted average
    total_mv = total_mv_merge_by_date.apply(lambda x : np.average(x,weights = x), axis = 1)
    total_mv_merge_by_date['average'] = total_mv
    cric_mv = cric_mv_merge_by_date.apply(lambda x : np.average(x,weights = x), axis = 1)
    cric_mv_merge_by_date['average'] = cric_mv
    
    
    plt.figure(1,figsize = (10,15))        
    plt.subplot(211)
    plt.plot(total_mv_merge_by_date['average'],label = 'total_mv')
    plt.xlabel('date')
    plt.ylabel('market value')
    plt.title('Stock ipo in ' + str(i))
    plt.legend()
    plt.subplot(212)
    plt.plot(cric_mv_merge_by_date['average'],label = 'cric_mv')
    plt.xlabel('date')
    plt.ylabel('market value')
    plt.legend()
    plt.savefig('/Users/Roy/Documents/Investment/Investment_lab/Stocks/index/market_value_plot/' + str(i))
    plt.show()











