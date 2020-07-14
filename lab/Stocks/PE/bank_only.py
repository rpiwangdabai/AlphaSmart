# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:22:13 2020

@author: Hicore
"""

import tushare as ts
import pandas as pd
from collections import deque
import numpy as np 
import matplotlib.pyplot as plt

ts.set_token('ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592')


pro = ts.pro_api()

'''------'''
list_data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# get infustry

industry = pro.index_classify(level='L3', src='SW')

industry_code =  industry[industry['industry_name'] == '银行']['index_code'].iloc[0]

industry_member = pro.index_member(index_code = industry_code)


'''------bank industry stock------'''


listed_bank = list_data[list_data['ts_code'].isin(industry_member['con_code']) ]
listed_bank = listed_bank.sort_values('list_date')

initial_date = '20030610'
end_date = '20200707'

total_pb_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 
total_pe_merge_by_date = pd.DataFrame(index = pd.date_range(initial_date,end_date,freq = 'B')) 

stock_ticks = deque(industry_member['con_code'])

while stock_ticks:

    # get tick and date
    tick = stock_ticks.popleft()
    
    daily_basic = pro.daily_basic(ts_code=tick, fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb,pe_ttm')
    # set trade date as index
    daily_basic['trade_date'] = pd.to_datetime(daily_basic['trade_date'])
    daily_basic.set_index('trade_date', inplace = True)
    
    # select columns
    selected_data_pb = pd.DataFrame(daily_basic['pb'])
    selected_data_pe_ttm = pd.DataFrame(daily_basic['pe_ttm'])
    
    # merge 
    total_pb_merge_by_date['pb_' + tick] = selected_data_pb
    total_pe_merge_by_date['pe_ttm_' + tick] = selected_data_pe_ttm


#  delete hoilday 
total_pb_merge_by_date = total_pb_merge_by_date.dropna(how = 'all')
total_pe_merge_by_date = total_pe_merge_by_date.dropna(how = 'all')
# fill na with fill
total_pb_merge_by_date = total_pb_merge_by_date.fillna(method = 'ffill', axis = 0)
total_pe_merge_by_date = total_pe_merge_by_date.fillna(method = 'ffill', axis = 0)
# fill initial zero value with 0
total_pb_merge_by_date = total_pb_merge_by_date.fillna(0)
total_pe_merge_by_date = total_pe_merge_by_date.fillna(0)

average_pb = np.sum(total_pb_merge_by_date.values,axis = 1) / (36 - (total_pb_merge_by_date == 0).astype(int).sum(axis=1))
average_pe = np.sum(total_pe_merge_by_date.values,axis = 1) / (36 - (total_pe_merge_by_date == 0).astype(int).sum(axis=1))

total_pb_merge_by_date['average_pb'] = average_pb
total_pe_merge_by_date['average_pe'] = average_pe

'''---plot---'''
plt.figure(1,figsize = (10,15))        
plt.subplot(211)
plt.plot(total_pb_merge_by_date['average_pb'],label = 'average pb')
plt.xlabel('date')
plt.ylabel('average pb')
plt.legend()
plt.subplot(212)
plt.plot(total_pe_merge_by_date['average_pe'],label = 'average_pe')
plt.xlabel('date')
plt.ylabel('average pe')
plt.legend()

plt.show()

'''-----individual stock-----'''

pb_name = total_pb_merge_by_date.columns
pe_name = total_pe_merge_by_date.columns

for i in range(len(pb_name) - 1):
    pb_data_sub = total_pb_merge_by_date[[pb_name[i],'average_pb']]
    pe_data_sub = total_pe_merge_by_date[[pe_name[i],'average_pe']]

    pb_data_sub = pb_data_sub[pb_data_sub[pb_name[i]] != 0]
    pe_data_sub = pe_data_sub[pe_data_sub[pe_name[i]] != 0]


    plt.figure(1,figsize = (25,35))        
    plt.subplot(211)
    plt.plot(pb_data_sub['average_pb'],label = 'average pb')
    plt.plot(pb_data_sub[pb_name[i]],label = pb_name[i])
    plt.xlabel('date')
    plt.ylabel('average pb')
    plt.title(pe_name[i])
    plt.legend()
    plt.subplot(212)
    plt.plot(pe_data_sub['average_pe'],label = 'average_pe')
    plt.plot(pe_data_sub[pe_name[i]],label = pe_name[i])
    plt.xlabel('date')
    plt.ylabel('average pe')
    plt.legend()
    address = 'C:/Users/Hicore/Desktop/plot/'  + pe_name[i]
    address = address.replace('.','')
    plt.savefig(address)
    plt.show()








