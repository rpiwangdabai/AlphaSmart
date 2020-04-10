#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:12:37 2020

@author: Roy
"""

from sqlalchemy import create_engine
import scipy.stats as st
import pandas as pd
import numpy as np
import math
import collections

'''-----------get fund data and calculate portfolio mean and std-----------'''
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

ticks = collections.deque(['002771.OF','002620.OF','001657.OF'])
i = 0
portfolio_log_ret = pd.DataFrame()
while ticks:
    #get fund data by ticks
    tick = ticks.popleft()
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    fund_init_date = fund_data.iloc[-1]['end_date']
    if i == 0:
        portfolio_log_ret['end_date'] = fund_data['end_date']
        portfolio_log_ret[tick] = fund_data['log_ret']
        closest_date = fund_init_date
    else:
        if fund_init_date >= closest_date:
            closest_date = fund_init_date
            portfolio_log_ret = portfolio_log_ret[portfolio_log_ret['end_date']
                                                  > closest_date]
            portfolio_log_ret[tick] = fund_data['log_ret']
        else:
            portfolio_log_ret[tick] = fund_data[fund_data['end_date'] > closest_date]['log_ret']
    i += 1


size = portfolio_log_ret.shape[0]
drop_row = [i for i in range(size-40,size)]
portfolio_log_ret = portfolio_log_ret.drop(drop_row)
portfolio_log_ret = portfolio_log_ret.drop(['end_date'],axis = 1)
portfolio_log_ret_mean = portfolio_log_ret.mean()
portfolio_log_ret_cov = portfolio_log_ret.cov() 

# monte carlo simulation portfolio price
initial_investment = 50000
days = 5
simulation_round = 10000
conf_level = 0.05
weights = np.array([0.52,0.3,0.18])

simulated_result = pd.DataFrame(index = [i for i in range(1,simulation_round + 1)])
simulated_result['days0'] = [initial_investment] * simulation_round
for i in range(1,days + 1):
    column = 'days' + str(i-1)
    column_new = 'days' + str(i)
    simulated_log_ret = np.random.multivariate_normal(portfolio_log_ret_mean, portfolio_log_ret_cov,simulation_round)
    simulated_result[column_new] = np.multiply(np.exp(np.dot(weights,np.array(simulated_log_ret).T)),simulated_result[column])
    
# monte carlo simulate purchase ratio
simulation_round = 10000
purchased_period = 5
purchase_weight = np.random.rand(simulation_round,purchased_period)

# each weight sum to 1
purchase_weight = purchase_weight.reshape(simulation_round,purchased_period) / np.array(purchase_weight.sum(axis = 1)).reshape(simulation_round,1)
simulated_result_array = np.array(simulated_result)[:,1:6]
avg_cost = np.multiply(simulated_result_array,purchase_weight).sum(axis = 1)


# analysis
sim_mean = simulated_result_array.mean(axis = 1)


diff = sim_mean - avg_cost

result = pd.DataFrame()
result['price_avg'] = sim_mean
result['avg_cost'] = avg_cost
result['diff'] = diff


selected_result = result[result['diff'] > 200]
index  = list(selected_result.index)


purchase_weight_dataframe = pd.DataFrame(purchase_weight,columns = simulated_result.columns[1:6] )

selected_simulated_data = simulated_result.iloc[[19,20]]
selected_weight = purchase_weight_dataframe.iloc[index]























    
    
    
    
    
    
    
    
    
    
    
    
    
    


    

