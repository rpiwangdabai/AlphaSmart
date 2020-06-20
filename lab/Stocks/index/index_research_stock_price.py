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

data_l = pd.read_csv('/Users/Roy/Documents/Investment/Investment_lab/Stocks/index/stock_ticks.csv')

'''----------analysis----------'''

for i in range(2005,2020):
    print('running stock ipo in %d' %i)


    start_time = int(str(i) + '0101')
    end_time = int(str(i + 1) + '0101')
    
    sorted_data = data_l[(data_l.list_date > start_time) & (data_l.list_date < end_time)].sort_values('list_date')
    
    # sorted_data = data_l[(data_l.list_date < start_time)].sort_values('list_date')
    
    stock_ticks = deque(sorted_data['ts_code'])
    
    initial_date = str(sorted_data.list_date.iloc[0])
    end_date = '20200608'
    
    total_mv_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
    cric_mv_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B'))
    stock_price_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 

    # get data and merge
    # create engine
    engine_mv = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic', 
                         encoding ='utf8')
    engine_stock_fq = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_hfq', 
                         encoding ='utf8')
    
    
    while stock_ticks:
        

        # get tick and date
        tick = stock_ticks.popleft()
        '''-------------------mv data-------------------'''       
        sql_cmd = "SELECT * FROM `" + tick + '`;'
        stock_data = pd.read_sql(sql=sql_cmd, con=engine_mv)
        # set trade date as index
        stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date'])
        stock_data.set_index('trade_date', inplace = True)
        # select columns
        selected_data_total_mv = pd.DataFrame(stock_data['total_mv'])
        selected_data_circ_mv = pd.DataFrame(stock_data['circ_mv'])
        # merge 
        total_mv_merge_by_date['total_mv_' + tick] = selected_data_total_mv
        cric_mv_merge_by_date['circ_mv_' + tick] = selected_data_circ_mv
        
        '''-------------------stock price data-------------------'''
        sql_cmd = "SELECT * FROM `" + tick + '_hfq`;'
        stock_data_qfq = pd.read_sql(sql=sql_cmd, con=engine_stock_fq)
        # set trade date as index
        stock_data_qfq['trade_date'] = pd.to_datetime(stock_data_qfq['trade_date'])
        stock_data_qfq.set_index('trade_date', inplace = True)               
        # select columns
        stock_price_qfq = pd.DataFrame(stock_data_qfq['close'])
        # merge 
        stock_price_merge_by_date['stock_price_hfq_' + tick] = stock_price_qfq

    
    #  delete hoilday 
    total_mv_merge_by_date = total_mv_merge_by_date.dropna(how = 'all')
    cric_mv_merge_by_date = cric_mv_merge_by_date.dropna(how = 'all')
    stock_price_merge_by_date = stock_price_merge_by_date.dropna(how = 'all')
    # fill na with fill
    total_mv_merge_by_date = total_mv_merge_by_date.fillna(method = 'ffill', axis = 0)
    cric_mv_merge_by_date = cric_mv_merge_by_date.fillna(method = 'ffill', axis = 0)
    stock_price_merge_by_date = stock_price_merge_by_date.fillna(method = 'ffill', axis = 0)
    # fill initial zero value with 0
    total_mv_merge_by_date = total_mv_merge_by_date.fillna(0)
    cric_mv_merge_by_date = cric_mv_merge_by_date.fillna(0)
    stock_price_merge_by_date = stock_price_merge_by_date.fillna(0)
    # calcualte weighted average
    weight_by_total_mv = (stock_price_merge_by_date.values * total_mv_merge_by_date.values).sum(axis = 1) / total_mv_merge_by_date.sum(axis = 1).values
    weight_by_cric_mv = (stock_price_merge_by_date.values * cric_mv_merge_by_date.values).sum(axis = 1) / cric_mv_merge_by_date.sum(axis = 1).values
    stock_price_merge_by_date['average_mv'] = weight_by_total_mv
    stock_price_merge_by_date['average_cv'] = weight_by_cric_mv
    
 
    # plot
    plt.figure(1,figsize = (10,15))        
    plt.subplot(211)
    plt.plot(stock_price_merge_by_date['average_mv'],label = 'weighted_by_total_mv')
    plt.xlabel('date')
    plt.ylabel('weighted prices hfq')
    plt.title('Stock ipo in ' + str(i))
    plt.legend()
    plt.subplot(212)
    plt.plot(stock_price_merge_by_date['average_cv'],label = 'weighted_by_cric_mv')
    plt.xlabel('date')
    plt.ylabel('weighted prices hfq')
    plt.legend()
    plt.savefig('/Users/Roy/Documents/Investment/Investment_lab/Stocks/index/stock_price_plot/hfq/' + str(i))
    plt.show()











