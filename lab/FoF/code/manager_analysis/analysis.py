#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 20:31:35 2020

@author: Roy
"""

from sqlalchemy import create_engine
import pandas as pd
import math
import collections


# get index data
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

sql_cmd = "SELECT * FROM `" + '399300.SZ' + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)
# date column rename 
index_data = index_data.rename(columns = {'trade_date' : 'end_date'})



'''-----------get fund data and calculate correlation with index-----------'''
# get funds ticks
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')
tables = engine.table_names()

correlation = pd.DataFrame(columns = ['Ticks','Correlation'])

# calculate fund cor
i = 1
while tables:
    name = tables.pop()
    
    if name == '399300.sz':
        continue
    

    # get fund data 
    sql_cmd = "SELECT * FROM `" + name + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    
    # left join 
    fund_and_index_data = fund_data.join(index_data.set_index('end_date'),
                                         on = 'end_date',how = 'left',
                                         lsuffix='_left', rsuffix='_right')
    # delete row the log ret is nan
    fund_and_index_data = fund_and_index_data.dropna(subset = ['log_ret_left','log_ret_right'])
    
    
    #calculate correlation
    cor = fund_and_index_data['log_ret_left'].corr(fund_and_index_data['log_ret_right'])
    
    correlation = correlation.append({'Ticks' : name , 'Correlation' : cor}, ignore_index = True)

    print(i)
    i += 1
    
correlation.to_csv('D:\RoyMa\Python\Investment\lab\FoF\code\manager_analysis\Fund_correlation.csv', index = False)

'''-----------get fund data and calculate sharp ratio, mean and std-----------'''

data = pd.read_csv('D:\RoyMa\Python\Investment\lab\FoF\code\manager_analysis\Fund_correlation.csv')
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

ticks = collections.deque(data['Ticks'])
sharp_ratio = []
mean = []
std = []
i = 1

while ticks:
    
    tick = ticks.popleft()
    
    #get fund data by ticks
    
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    
    # drop log ret nan
    fund_data = fund_data.dropna(subset = ['log_ret'])
    # calculate log ret mean
    log_ret_mean = fund_data['log_ret'].mean()
    #calculate log ret std
    log_ret_std = fund_data['log_ret'].std()
    #calculate sharp ratio
    sharp_ratio_fund = log_ret_mean / log_ret_std * math.sqrt(252)
    
    sharp_ratio.append(sharp_ratio_fund)
    mean.append(log_ret_mean)
    std.append(log_ret_std)
    
    print(i)
    i += 1 


data['sharp_ration'] = sharp_ratio
data['mean'] = mean
data['std'] = std


data.to_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/cor_sharp_mean_std.csv',index = False)

# =============================================================================
# 300 mean std and sharp ratio
# =============================================================================




