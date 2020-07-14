#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:57:54 2020

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


stock_data = stock_data['20160101':]

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

# data = np.column_stack([log_return_daily, log_return_5_days, daily_open_close_change_log,
#                         daily_high_low_change_log,daily_vol_change_log,daily_amount_change_log])

data = np.column_stack([log_return_daily, daily_open_close_change_log,
                        daily_high_low_change_log])


data = pd.DataFrame(data,index = stock_data['trade_date']).dropna()



'''--------rolling training method 2--------'''

# def rolling_compare(target_score, history_sequences,model):
#     '''
    
#     Parameters
#     ----------
#     target_score : float
#         target sequences log likelihood, using models.scores.
#     history_sequences : np.ndarray
#         histry price to find the most similar sequences.
#     model : hmmlearn.hmm.GaussianHMM
#         trained hmm model.

#     Returns
#     -------
#     Top 10 Best possible result.

#     '''
    
#     index = []
#     history_score_diff = []
#     possible_value = []

#     for i in range(len(history_sequences) - 5):
        
#         history_sequences_epochs = history_sequences[i : 5 + i]
        
#         history_scores = model.score(history_sequences_epochs)
        
#         diff = abs(history_scores - target_score)
        
#         history_score_diff.append(diff)
        
#         index.append(i)
        
#     df = pd.DataFrame(history_score_diff,index = index)
    
#     df = df.sort_values(by = 0)
    
#     top_10 = list(df.index)[:10]
        
#     for value in top_10:
#         possible_value.append(history_sequences[value + 5][0])
            
    
#     possible_value = np.array(possible_value)
#     possible_value = (possible_value > 0).astype('int64')
    
#     if possible_value.sum() >= 6:
#         return 1
#     else:
#         return 0
    
def rolling_compare(target_score, history_sequences,model):
    '''
    
    Parameters
    ----------
    target_score : float
        target sequences log likelihood, using models.scores.
    history_sequences : np.ndarray
        histry price to find the most similar sequences.
    model : hmmlearn.hmm.GaussianHMM
        trained hmm model.

    Returns
    -------
    Best possible result.

    '''
    
    index = 0
    minimal_score = np.inf
    found_sequences = np.nan
    
    for i in range(len(history_sequences) - 5):
        
        history_sequences_epochs = history_sequences[i : 5 + i]
        
        history_scores = model.score(history_sequences_epochs)
        
        diff = abs(history_scores - target_score)
        
        if diff < minimal_score:
            
            minimal_score = diff
            
            index = i
            
            found_sequences = history_sequences[i : 5 + i]
    
    return history_sequences[5 + index],index, minimal_score, found_sequences

# def rolling_compare(target_score, history_sequences,model):
#     '''
    
#     Parameters
#     ----------
#     target_score : float
#         target sequences log likelihood, using models.scores.
#     history_sequences : np.ndarray
#         histry price to find the most similar sequences.
#     model : hmmlearn.hmm.GaussianHMM
#         trained hmm model.

#     Returns
#     -------
#     Best possible result.

#     '''
    
#     index = 0
#     minimal_score = np.inf
#     found_sequences = np.nan
    
#     for i in range(len(history_sequences) - 5):
        
#         history_sequences_epochs = history_sequences[i : 5 + i]
        
#         history_scores = model.score(history_sequences_epochs)
        
#         diff = abs(history_scores - target_score)
        
#         if diff < minimal_score:
            
#             minimal_score = diff
            
#             index = i
            
#             found_sequences = history_sequences[i : 5 + i]
            
#     log_return_change_percentage = history_sequences[5 + index][0] - history_sequences[4 + index][0]

#     return log_return_change_percentage ,index, minimal_score, found_sequences



training_rolling_data = data['2016-01-01':'2019-01-01'].values
test_rolling_data = data['2019-01-01':].values
history_sequences = data[:'2018-12-31'].values

# Train and compare,  T = 5

train_for_predict_dataset = np.r_[training_rolling_data[-100:],test_rolling_data]


predict_set = []
index_set = []
minimal_score_set = []
same_sequences_set = []
target_sequences_set = []


for i in range(len(test_rolling_data)):
    
    train_data_epochs = train_for_predict_dataset[i:100+i]
    
    
        
    model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full')

    model.fit(train_data_epochs)
    
    while model.transmat_.sum() != 3:
        
        model.fit(train_data_epochs)
        
        
    current_score = model.score(train_data_epochs[-5:])
    
    target_sequences_set.append(train_data_epochs[-5:])

    predict_next_day, index, minimal_score, found_sequences = rolling_compare(current_score,history_sequences,model)
    
    predict_set.append(train_data_epochs[-1][0] + predict_next_day)

    index_set.append(index)

    minimal_score_set.append(minimal_score)
    
    same_sequences_set.append(found_sequences)



predict_set_array = np.array(predict_set) 
    
'''--------------metrics--------------'''


import sklearn

predict_set_dataframe = pd.DataFrame(predict_set_array, columns = [1,2,3])
test_set_dataframe = pd.DataFrame(test_rolling_data, columns = [1,2,3])

  
# transform to 0/1

test_ = (test_set_dataframe[1] > 0).astype('int64')[:247]
predict_ = (predict_set_dataframe[1] > 0).astype('int64')

print('----------------------------------------')
accuracy_score = sklearn.metrics.accuracy_score(test_, predict_)
print('accuracy_score for {} is {}'.format(i,accuracy_score))
classification_report = sklearn.metrics.classification_report(test_, predict_)
print('classification_report for {} is following'.format(i))
print(classification_report)
confusion_matrix = sklearn.metrics.confusion_matrix(test_, predict_)
print('accuracy_score for {} is following'.format(i))
print(confusion_matrix)
    

for i in range(200):

    plt.plot(same_sequences_set[i][:,0])
    plt.plot(target_sequences_set[i][:,0])
    plt.show()
    time.sleep(10)











