#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 23:31:57 2020

@author: Roy
"""

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
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_hfq', 
                     encoding ='utf8')

sql_cmd = "SELECT * FROM `" + '000001.SZ_hfq' + '`;'
stock_data = pd.read_sql(sql=sql_cmd, con=engine)
# date column rename 
stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date'])
stock_data = stock_data.set_index('trade_date',drop = False)
stock_data = stock_data[::-1]
stock_data = stock_data.dropna()


# index_data = index_data['20160101':]

# daily log return
log_return_daily = np.log(stock_data.close) - np.log(stock_data.close.shift(1))

# 5 day log return
log_return_5_days = np.log(stock_data.close) - np.log(stock_data.close.shift(5))

# daily open close change log return
daily_open_close_change_log = np.log(stock_data.close) - np.log(stock_data.open)

# daily high low change log return
daily_high_low_change_log = np.log(stock_data.high) - np.log(stock_data.close)

# daily vol log change
daily_vol_change_log = np.log(stock_data.vol) - np.log(stock_data.vol.shift(1))

# daily amount log change
daily_amount_change_log = np.log(stock_data.amount) - np.log(stock_data.amount.shift(1))

data = np.column_stack([log_return_daily, log_return_5_days, daily_open_close_change_log,
                        daily_high_low_change_log,daily_vol_change_log,daily_amount_change_log])



data = pd.DataFrame(data,index = stock_data['trade_date']).dropna()

# data = data[:100]
train_data = data.values



# Make an HMM instance and execute fit
model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data)

# Predict the optimal sequence of internal hidden state
test_data = data[:1900]

hidden_states = model.predict(train_data[::-1])

#plot
tradeDate = pd.to_datetime(data.index)
closeIndex = stock_data.loc[data.index]['close']



plt.figure(figsize=(105, 55))  
for i in range(model.n_components):
    if i == 0:
        color = 'red'
    elif i ==1 :
        color = 'y'
    else:
        color = 'b'
    idx = (hidden_states==i)
    plt.plot_date(tradeDate[idx],closeIndex[idx],'o',label='%dth hidden state'%i,lw=1,color = color)
    plt.legend()
    plt.grid(1)

plt.savefig('/Users/Roy/Desktop/Figure_1.png')




from matplotlib.dates import YearLocator, MonthLocator
fig, axs = plt.subplots(3, sharex=True, sharey=True)
colours = cm.rainbow(np.linspace(0, 1, 4))

one_layer = []
two_layer = []
three_layer = []
fourth_layer = []

for i, (ax, colour) in enumerate(zip(axs, colours)):
    # Use fancy indexing to plot data in each state.
    mask = hidden_states == i
    ax.plot_date(tradeDate[mask], closeIndex[mask], ".-", c=colour)
    ax.set_title("{0}th hidden state".format(i))

    # Format the ticks.
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_minor_locator(MonthLocator())

    ax.grid(True)

plt.show()






















