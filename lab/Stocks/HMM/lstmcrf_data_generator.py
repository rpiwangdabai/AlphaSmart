#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:38:28 2020

@author: Roy
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:11:40 2020

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
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/index', 
                     encoding ='utf8')

sql_cmd = "SELECT * FROM `" + '399300.SZ' + '`;'
index_data = pd.read_sql(sql=sql_cmd, con=engine)

# set trade data as datetimeindex
index_data.set_index('trade_date', inplace = True)
index_data.index = pd.DatetimeIndex(index_data.index)
index_data = index_data.iloc[::-1]



# 5 day log return
index_data['log_return_5_days'] = np.log(index_data.close) - np.log(index_data.close.shift(5))

# daily open close change log return
index_data['daily_open_close_change_log'] = np.log(index_data.close) - np.log(index_data.open)

# daily high low change log return
index_data['daily_high_low_change_log'] = np.log(index_data.high) - np.log(index_data.close)

# delete index related columns

train_data = index_data.drop(['close','open','high','low','pre_close'], axis=1)

# trainning_data
train_data = train_data['2016-03':].values
train_data = train_data[:,1:]


# Make an HMM instance and execute fit
model = GaussianHMM(n_components=3, n_iter=1000).fit(train_data)
# # Predict the optimal sequence of internal hidden state
# test_data = data[:1900,:]

hidden_states = model.predict(train_data)

#plot
tradeDate = pd.to_datetime(index_data['2016-03':].index)
closeIndex = index_data['2016-03':]['close']



plt.figure(figsize=(15, 8))  
for i in range(model.n_components):
    idx = (hidden_states==i)
    plt.plot_date(tradeDate[idx],closeIndex[idx],'.',label='%dth hidden state'%i,lw=1)
    plt.legend()
    plt.grid(1)


# # rcf train data
# rcf_train_data = index_data['2016-03':]
# rcf_train_data['hidden_states'] = hidden_states

# rcf_train_data.to_csv('/Users/Roy/Documents/Investment/Investment_lab/Stocks/code/HMM/data/without_index_data/lstmcrfdata_15_withoutindex.csv')

















