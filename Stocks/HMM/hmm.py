#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 22:52:35 2020

@author: Roy
"""
import tushare as ts 
import pandas as pd
from sqlalchemy import create_engine
import math



from hmmlearn.hmm import GaussianHMM,GMMHMM
import datetime
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import seaborn as sns
sns.set_style('white')




# get index data
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/index', 
                     encoding ='utf8')

sql_cmd = "SELECT * FROM `" + '399300.SZ' + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)
# date column rename 
index_data = index_data.rename(columns = {'trade_date' : 'end_date'})


# 5 day log return
log_return_5_days = np.log(index_data.close) - np.log(index_data.close.shift(-5))

# daily open close change log return
daily_open_close_change_log = np.log(index_data.close) - np.log(index_data.open)

# daily high low change log return
daily_high_low_change_log = np.log(index_data.high) - np.log(index_data.close)


data = np.column_stack([index_data.log_ret, log_return_5_days, daily_open_close_change_log,
                        daily_high_low_change_log,index_data.vol,index_data.amount])

train_data = data[:3687,:]


# Make an HMM instance and execute fit
model = GaussianHMM(n_components=5, covariance_type="full", n_iter=1000).fit(train_data)
# Predict the optimal sequence of internal hidden state
test_data = data[:1900,:]

hidden_states = model.predict(train_data[::-1])

#plot
tradeDate = pd.to_datetime(index_data['end_date'][:3687])
closeIndex = index_data['close'][:3687]



plt.figure(figsize=(15, 8))  
for i in range(model.n_components):
    idx = (hidden_states==i)
    plt.plot_date(tradeDate[idx],closeIndex[idx],'.',label='%dth hidden state'%i,lw=1)
    plt.legend()
    plt.grid(1)






