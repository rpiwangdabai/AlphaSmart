#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 23:07:33 2020

@author: Roy
"""

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
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

'''------行业分类------'''

token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'
ts.set_token(token)
ts_pro = ts.pro_api()

industrial_classify = ts_pro.index_classify(level='L2', src='SW')
industrial_classify_index_code = industrial_classify['index_code']
# 行业循环
for i,code in enumerate(industrial_classify_index_code):
    
    index_member = ts_pro.index_member(index_code = code)
    index_member_sorted_by_date = index_member.sort_values('in_date')
    
    stock_ticks = deque(index_member_sorted_by_date['con_code'])
    
    initial_date = str(index_member_sorted_by_date.in_date.iloc[0])
    end_date = '20200706'
    
    total_pe_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
    total_pb_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
    # get data and merge
    # create engine
    engine_pe = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic', 
                         encoding ='utf8')
    
    stock_nums = len(stock_ticks)
    
    while stock_ticks:
        
        # get tick and date
        tick = stock_ticks.popleft()
        '''-------------------pe data-------------------'''       
        sql_cmd = "SELECT * FROM `" + tick + '`;'
        stock_data = pd.read_sql(sql=sql_cmd, con=engine_pe)
        # set trade date as index
        stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date'])
        stock_data.set_index('trade_date', inplace = True)
        # select columns
        selected_data_pe_ttm = pd.DataFrame(stock_data['pe_ttm'])
        selected_data_pb = pd.DataFrame(stock_data['pb'])

        # merge 
        total_pe_merge_by_date['pe_ttm_' + tick] = selected_data_pe_ttm
        total_pb_merge_by_date['pb_' + tick] = selected_data_pb
        
    
    #  delete hoilday 
    total_pe_merge_by_date = total_pe_merge_by_date.dropna(how = 'all')
    total_pb_merge_by_date = total_pb_merge_by_date.dropna(how = 'all')
    
    # fill na with fill
    total_pe_merge_by_date = total_pe_merge_by_date.fillna(method = 'ffill', axis = 0)
    total_pb_merge_by_date = total_pb_merge_by_date.fillna(method = 'ffill', axis = 0)
    
    # fill initial zero value with 0
    total_pe_merge_by_date = total_pe_merge_by_date.fillna(0)
    total_pb_merge_by_date = total_pb_merge_by_date.fillna(0)

    # calcualte weighted average
    
    average_pe = np.sum(total_pe_merge_by_date.values,axis = 1) / (stock_nums - (total_pe_merge_by_date == 0).astype(int).sum(axis=1))
    average_pb = np.sum(total_pb_merge_by_date.values,axis = 1) / (stock_nums - (total_pb_merge_by_date == 0).astype(int).sum(axis=1))
    
    total_pe_merge_by_date['average_pe'] = average_pe
    total_pb_merge_by_date['average_pb'] = average_pb

    '''---plot---'''
    plt.figure(1,figsize = (10,15))        
    plt.subplot(211)
    plt.plot(total_pb_merge_by_date['average_pb'],label = 'average pb')
    plt.xlabel('date')
    plt.ylabel('average pb')
    plt.title(code)
    plt.legend()
    plt.subplot(212)
    plt.plot(total_pe_merge_by_date['average_pe'],label = 'average_pe')
    plt.xlabel('date')
    plt.ylabel('average pe')
    plt.legend()
    plt.savefig('/Users/Roy/Documents/Investment/lab/Stocks/PE/二级分类/' + industrial_classify.iloc[i]['industry_name'])
    plt.show()

    











