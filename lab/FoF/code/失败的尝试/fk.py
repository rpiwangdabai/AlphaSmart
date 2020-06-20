#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 22:16:00 2020

@author: Roy
"""

i = 0
while ticks:
    #get fund data by ticks
    tick = ticks.popleft()
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    if i == 0:
        portfolio_data = pd.read_sql(sql=sql_cmd, con=engine)
        portfolio_data = portfolio_data[['end_date','log_ret']]
    else:
        fund_data = pd.read_sql(sql=sql_cmd, con=engine)
        if portfolio_data.shape[0] < fund_data.shape[0]:
            left = portfolio_data
            right = fund_data[['end_date','log_ret']]
        else:
            left = fund_data[['end_date','log_ret']]
            right = portfolio_data
              
        portfolio_data = pd.merge(left,right,on = ['end_date'], how = 'left')
    portfolio_data = portfolio_data.rename(columns = {'log_ret' : tick})
    portfolio_data = portfolio_data.dropna()
    i += 1

