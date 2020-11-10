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

window = 5

while ticks:
    
    tick = ticks.popleft()
    
    #get fund data by ticks
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    
    # init date and end data
    fund_data = fund_data[::-1]
    fund_data['cum_return'] =  fund_data['log_ret'].rolling(window = window).sum()
    fund_data = fund_data.dropna(subset=['cum_return'])
    
    fund_data_smooth = fund_data.iloc[::window]
    
    
    
    # # drop log ret nan
    # fund_data_smooth = fund_data_smooth.dropna(subset = ['log_ret'])
    # calculate log ret mean
    log_ret_mean = fund_data_smooth['log_ret'].mean()
    #calculate log ret std
    log_ret_std = fund_data_smooth['log_ret'].std()
    #calculate sharp ratio
    sharp_ratio_fund = log_ret_mean / log_ret_std * math.sqrt(252)
    
    sharp_ratio.append(sharp_ratio_fund)
    mean.append(log_ret_mean)
    std.append(log_ret_std)
    
    print(i)
    i += 1 


data['sharp_ratio'] = sharp_ratio
data['mean'] = mean
data['std'] = std


data.to_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/cor_sharp_mean_std.csv',index = False)

# =============================================================================
# 300 mean std and sharp ratio
# =============================================================================
tick = '399300.sz'

sql_cmd = "SELECT * FROM `" + tick + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)

# drop log ret nan
index_data = index_data.dropna(subset = ['log_ret'])
# calculate log ret mean
log_ret_mean = index_data['log_ret'].mean()
#calculate log ret std
log_ret_std = index_data['log_ret'].std()
#calculate sharp ratio
sharp_ratio_index = log_ret_mean / log_ret_std * math.sqrt(252)

# =============================================================================
# set criteria
# =============================================================================
data = pd.read_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/cor_sharp_mean_std.csv')

selected_data = data[(data['mean'] > 3 * log_ret_mean) & 
                    (data['std'] <   log_ret_std) &
                    (data['sharp_ratio'] >  sharp_ratio_index)]

selected_data.to_csv('D:\RoyMa\Python\Investment\lab\FoF\code\manager_analysis\selected_fund_by_sharp.csv',index = False)







# =============================================================================
# ------analysis strategy two ------
# =============================================================================
# get index data
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

sql_cmd = "SELECT * FROM `" + '399300.SZ' + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)
# date column rename 
index_data = index_data.rename(columns = {'trade_date' : 'end_date'})


'''-----------layer one-----------'''
'''-----------get fund data and calculate correlation with index-----------'''
# get funds ticks
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')
tables = engine.table_names()

sharp_1 = pd.DataFrame(columns = ['Ticks','diff_sharp'])

# calculate fund log return - index log return sharp ratio and named as sharp_1
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
    #calculate diff
    fund_and_index_data['diff'] = fund_and_index_data['log_ret_left'] - fund_and_index_data['log_ret_right']
    
    log_ret_diff_mean = fund_and_index_data['diff'].mean()
    #calculate log ret std
    log_ret_diff_std = fund_and_index_data['diff'].std()
    #calculate sharp ratio
    log_ret_diff_sharp_ratio = log_ret_diff_mean / log_ret_diff_std * math.sqrt(252)    
    sharp_1 = sharp_1.append({'Ticks' : name , 'diff_sharp' : log_ret_diff_sharp_ratio}, ignore_index = True)

    print(i)
    i += 1
    
sharp_1.to_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2\sharp_1.csv', index = False)



'''-----------layer_two-----------'''
'''-----------get fund data and calculate sharp ratio, mean and std-----------'''

data = pd.read_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2/sharp_1.csv')
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

data = data[data['diff_sharp'] > 0]


ticks = collections.deque(data['Ticks'])
sharp_ratio = []
mean = []
std = []
i = 1

window = 5

while ticks:
    
    tick = ticks.popleft()
    
    #get fund data by ticks
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    
    # init date and end data
    fund_data = fund_data[::-1]
    fund_data['cum_return'] =  fund_data['log_ret'].rolling(window = window).sum()
    fund_data = fund_data.dropna(subset=['cum_return'])
    
    fund_data_smooth = fund_data.iloc[::window]
    
    
    
    # # drop log ret nan
    # fund_data_smooth = fund_data_smooth.dropna(subset = ['log_ret'])
    # calculate log ret mean
    log_ret_mean = fund_data_smooth['log_ret'].mean()
    #calculate log ret std
    log_ret_std = fund_data_smooth['log_ret'].std()
    #calculate sharp ratio
    sharp_ratio_fund = log_ret_mean / log_ret_std * math.sqrt(252)
    
    sharp_ratio.append(sharp_ratio_fund)
    mean.append(log_ret_mean)
    std.append(log_ret_std)
    
    print(i)
    i += 1 


data['sharp_ratio'] = sharp_ratio
data['mean'] = mean
data['std'] = std


data.to_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2/diff_sharp_mean_std.csv',index = False)

# =============================================================================
# 300 mean std and sharp ratio
# =============================================================================
tick = '399300.sz'

sql_cmd = "SELECT * FROM `" + tick + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)

# drop log ret nan
index_data = index_data.dropna(subset = ['log_ret'])
# calculate log ret mean
log_ret_mean = index_data['log_ret'].mean()
#calculate log ret std
log_ret_std = index_data['log_ret'].std()
#calculate sharp ratio
sharp_ratio_index = log_ret_mean / log_ret_std * math.sqrt(252)

# =============================================================================
# set criteria
# =============================================================================
data = pd.read_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2/diff_sharp_mean_std.csv')

selected_data = data[(data['mean'] > 3 * log_ret_mean) & 
                    (data['std'] <   log_ret_std) &
                    (data['sharp_ratio'] >  sharp_ratio_index)]

selected_data.to_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2/selected_fund_by_sharp.csv',index = False)











