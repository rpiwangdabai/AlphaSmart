#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 16:55:24 2020

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
index_data['end_date'] = pd.to_datetime(index_data['end_date'])
index_data = index_data.set_index('end_date',drop = False)
index_data = index_data[::-1]


# index_data = index_data['20160101':]

# 5 day log return
log_return_5_days = np.log(index_data.close) - np.log(index_data.close.shift(5))

# daily open close change log return
daily_open_close_change_log = np.log(index_data.close) - np.log(index_data.open)

# daily high low change log return
daily_high_low_change_log = np.log(index_data.high) - np.log(index_data.close)

# daily vol log change
daily_vol_change_log = np.log(index_data.vol) - np.log(index_data.vol.shift(1))

# daily amount log change
daily_amount_change_log = np.log(index_data.amount) - np.log(index_data.amount.shift(1))

data = np.column_stack([index_data.log_ret, log_return_5_days, daily_open_close_change_log,
                        daily_high_low_change_log,daily_vol_change_log,daily_amount_change_log])

data = index_data.log_ret
data = pd.DataFrame(data,index = pd.to_datetime(index_data['end_date'])).dropna()



'''--------rolling training method 2--------'''

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
            
            found_sequences = history_sequences[i : 6 + i]
    
    return history_sequences[5 + index],index, minimal_score, found_sequences



training_rolling_data = data['2016-01-01':'2019-01-01'].values
test_rolling_data = data['2019-01-01':].values
history_sequences = data[:'2018-12-31'].values

# rolling training for initial s,t,e
train_data_epochs = training_rolling_data[:100]
model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data_epochs)

initial_start_prob = model.startprob_
initial_transmat = model.transmat_


for i in range(1,len(training_rolling_data) - 99):
    
    train_data_epochs = training_rolling_data[i:100+i]
   
    
    
    model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full')
    
    
    try:
        model.fit(train_data_epochs)
    except ValueError:
        model.fit(train_data_epochs)
    


    

    

# 和训练集没有重复， T = 5

train_for_predict_dataset = np.r_[training_rolling_data[-100:],test_rolling_data]

predict_set = []
index_set = []
minimal_score_set = []
same_sequences_set = []
target_sequences_set = []

for i in range(len(test_rolling_data) + 1):
    
    train_data_epochs = train_for_predict_dataset[i:100+i]
       
    model_p = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full')
    
    model_p.fit(train_data_epochs)
    
    while model_p.transmat_.sum() != 3:
        
        model_p.fit(train_data_epochs)
        

    
    
    current_score = model_p.score(train_data_epochs[-5:])

    target_sequences_set.append(train_data_epochs[-6:])

    predict_next_day, index, minimal_score, found_sequences = rolling_compare(current_score,history_sequences,model_p)

    predict_set.append(predict_next_day)

    index_set.append(index)

    minimal_score_set.append(minimal_score)
    
    same_sequences_set.append(found_sequences)
    
del predict_set[-1]
predict_set_array = np.array(predict_set) 
    
'''--------------metrics--------------'''


import sklearn
#
predict_set_dataframe = pd.DataFrame(predict_set_array, columns = [1,2,3,4,5,6])

test_set_dataframe = pd.DataFrame(test_rolling_data, columns = [1,2,3,4,5,6])

for i in range(1,7):
    
    # transform to 0/1
    predict_ = (predict_set_dataframe[i] > 0).astype('int64')
    test_ = (test_set_dataframe[i] > 0).astype('int64')
    
    
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

    plt.plot(same_sequences_set[i])
    plt.plot(target_sequences_set[i])
    plt.show()









