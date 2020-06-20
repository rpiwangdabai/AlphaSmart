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


data = pd.DataFrame(data,index = pd.to_datetime(index_data['end_date'])).dropna()

# data = data[:100]
# train_data = data.values


# '''------mutiple variables------'''
# steps_per_sample = 20
# samples = len(train_data) // steps_per_sample  
# remainder = len(train_data) % steps_per_sample
# if remainder != 0:
#     lengths = [steps_per_sample] * samples + [remainder]
# else:
#     lengths = [steps_per_sample] * samples



# Make an HMM instance and execute fit
# model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data)

# Predict the optimal sequence of internal hidden state
# test_data = data[:1900,:]

# hidden_states = model.predict(train_data[::-1])

# #plot
# tradeDate = pd.to_datetime(data.index)
# closeIndex = index_data.loc[data.index]['close']



# plt.figure(figsize=(105, 55))  
# for i in range(model.n_components):
#     if i == 0:
#         color = 'red'
#     elif i ==1 :
#         color = 'y'
#     else:
#         color = 'b'
#     idx = (hidden_states==i)
#     plt.plot_date(tradeDate[idx],closeIndex[idx],'o',label='%dth hidden state'%i,lw=1,color = color)
#     plt.legend()
#     plt.grid(1)

# plt.savefig('/Users/Roy/Desktop/Figure_1.png')



# def aic(likelihood, p):
#     '''
#     Parameters
#     ----------
#     likelihood : float
#         likelihood function of the model.
#     p : int
#         Number of estimated parameters in the model.

#     Returns
#     -------
#     aic_score: AIC score
#     '''
    
#     aic_score = -2 * likelihood + 2 * p
#     return aic_score

# def bic(likelihood, p, m):
#     '''
#     Parameters
#     ----------
#     likelihood : float
#         likelihood function of the model.
#     p : int
#         Number of estimated parameters in the model.
#     m : int
#         number of observation points.

#     Returns
#     -------
#     bic_score: BIC score.
#     '''
    
#     bic_score = -2 * likelihood + p * math.log(m)
#     return bic_score

# aic_ = []
# bic_ = []

# for i in range(2,100):
    
#     model = GaussianHMM(n_components=i, n_iter=1000,covariance_type = 'full').fit(train_data)

#     likelihood = model.score(train_data)
#     m = train_data.size
#     p =  * i * i + i * 2
#     aic_.append(aic(likelihood,p))
#     bic_.append(bic(likelihood,p,m))
    
# '''-------determined time lengths-------'''

# test = data[500:600]
# score = []
# for i in range(100):
    
#     data_ = data[:10 + i]
#     train_data = data_.values

#     # Make an HMM instance and execute fit
#     model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data)
#     score.append(model.score(test))
    
# '''-------rolling training-------'''
# test_data = data['2019-01-01':].values

# train_data = data[:'2019-01-01'].values
# train_data_epochs = train_data[:100]
# model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data_epochs)

# initial_start_prob = model.startprob_
# initial_transmat = model.transmat_
# initial_means = model.means_
# initial_covars = model.covars_

# # monitor_score
# score_ = []

# for i in range(1,430):
    
#     train_data_epochs = train_data[i:100+i]
   
#     model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                         startprob_prior = initial_start_prob,
#                         transmat_prior = initial_transmat,
#                         means_prior = initial_means,
#                         covars_prior = initial_covars,
#                         init_params = ' ' ).fit(train_data_epochs)
    
#     # model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data_epochs)

    
#     initial_start_prob = model.startprob_
#     initial_transmat = model.transmat_
#     initial_means = model.means_
#     initial_covars = model.covars_
    
#     score_.append(model.score(test_data))
    
#     i += 1 
    
# plt.plot(score_)
    
# '''-------predict-------'''

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
    
#     for i in range(len(history_sequences) - 100):
        
#         history_sequences_epochs = history_sequences[i : 100 + i]
        
#         history_scores = model.score(history_sequences_epochs)
        
#         diff = abs(history_scores - target_score)
        
#         if diff < minimal_score:
            
#             minimal_score = diff
            
#             index = i
    
#     return history_sequences[100 + index],index, minimal_score


# predict_set = []

# index_set = []

# minimal_score_set = []

# i_set = []

# begin_index = len(data) - len(test_data)

# i_set = []


# for i in range(len(test_data)):
    
#     initial_sequences = data[begin_index - 100 + i : begin_index + i]
    
#     current_score = model.score(initial_sequences)
    
#     predict_next_day, index, minimal_score = rolling_compare(current_score,train_data,model)
    
#     predict_set.append(predict_next_day)

#     index_set.append(index)

#     minimal_score_set.append(minimal_score)
    
#     i_set.append(begin_index - 100 + i)


# predict_set_array = np.array(predict_set)

# rolling with predict value

# initial_sequences = train_data[-100:]

# for i in range(len(test_data)):
    
#     current_score = model.score(initial_sequences)
    
#     predict_next_day, index, minimal_score = rolling_compare(current_score,train_data,model)
    
#     initial_sequences = np.r_[initial_sequences,[predict_next_day]]
    
#     initial_sequences = initial_sequences[-100:]
    
#     predict_set.append(predict_next_day)

#     index_set.append(index)

#     minimal_score_set.append(minimal_score)
    
#     i_set.append(begin_index - 100 + i)


# predict_set_array = np.array(predict_set)

# '''--------------metrics--------------'''


# import sklearn
# #
# predict_set_dataframe = pd.DataFrame(predict_set_array, columns = [1,2,3,4,5,6])

# test_set_dataframe = pd.DataFrame(test_data, columns = [1,2,3,4,5,6])

# for i in range(1,7):
    
#     # transform to 0/1
#     predict_ = (predict_set_dataframe[i] > 0).astype('int64')
#     test_ = (test_set_dataframe[i] > 0).astype('int64')
    
    
#     print('----------------------------------------')
#     accuracy_score = sklearn.metrics.accuracy_score(test_, predict_)
#     print('accuracy_score for {} is {}'.format(i,accuracy_score))
#     classification_report = sklearn.metrics.classification_report(test_, predict_)
#     print('classification_report for {} is following'.format(i))
#     print(classification_report)
#     confusion_matrix = sklearn.metrics.confusion_matrix(test_, predict_)
#     print('accuracy_score for {} is following'.format(i))
#     print(confusion_matrix)


# '''--------rolling training method 2--------'''

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
    
#     for i in range(len(history_sequences) - 5):
        
#         history_sequences_epochs = history_sequences[i : 5 + i]
        
#         history_scores = model.score(history_sequences_epochs)
        
#         diff = abs(history_scores - target_score)
        
#         if diff < minimal_score:
            
#             minimal_score = diff
            
#             index = i
    
#     return history_sequences[5 + index],index, minimal_score



# training_rolling_data = data['2016-01-01':'2019-01-01'].values
# test_rolling_data = data['2019-01-01':].values
# history_sequences = data[:'2018-12-31'].values

# # rolling training for initial s,t,e
# train_data_epochs = training_rolling_data[:100]
# model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data_epochs)

# initial_start_prob = model.startprob_
# initial_transmat = model.transmat_
# initial_means = model.means_
# initial_covars = model.covars_


# for i in range(1,len(training_rolling_data) - 99):
    
#     train_data_epochs = training_rolling_data[i:100+i]
   
#     model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                         startprob_prior = initial_start_prob,
#                         transmat_prior = initial_transmat,
#                         means_prior = initial_means,
#                         covars_prior = initial_covars,
#                         init_params = ' ' ).fit(train_data_epochs)
    
#     # model = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full').fit(train_data_epochs)

    
#     initial_start_prob = model.startprob_
#     initial_transmat = model.transmat_
#     initial_means = model.means_
#     initial_covars = model.covars_
    

    

# # 和训练集没有重复， T = 10

# train_for_predict_dataset = np.r_[training_rolling_data[-100:],test_rolling_data]

# predict_set = []
# index_set = []
# minimal_score_set = []

# for i in range(len(test_rolling_data) + 1):
    
#     train_data_epochs = train_for_predict_dataset[i:100+i]
   
        
#     model_p = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                         startprob_prior = initial_start_prob,
#                         transmat_prior = initial_transmat,
#                         means_prior = initial_means,
#                         covars_prior = initial_covars,
#                         init_params = ' ' ).fit(train_data_epochs)
    
#     while model_p.transmat_.sum() != 3:
        
#         model_p = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                     startprob_prior = initial_start_prob,
#                     transmat_prior = initial_transmat,
#                     means_prior = initial_means,
#                     covars_prior = initial_covars,
#                     init_params = ' ' ).fit(train_data_epochs)
        
#     initial_start_prob = model_p.startprob_
#     initial_transmat = model_p.transmat_
#     initial_means = model_p.means_
#     initial_covars = model_p.covars_
    
    
#     current_score = model_p.score(train_data_epochs[-5:])

#     predict_next_day, index, minimal_score = rolling_compare(current_score,history_sequences,model_p)

#     predict_set.append(predict_next_day)

#     index_set.append(index)

#     minimal_score_set.append(minimal_score)
    
# del predict_set[-1]
# predict_set_array = np.array(predict_set) 
    
# '''--------------metrics--------------'''


# import sklearn
# #
# predict_set_dataframe = pd.DataFrame(predict_set_array, columns = [1,2,3,4,5,6])

# test_set_dataframe = pd.DataFrame(test_rolling_data, columns = [1,2,3,4,5,6])

# for i in range(1,7):
    
#     # transform to 0/1
#     predict_ = (predict_set_dataframe[i] > 0).astype('int64')
#     test_ = (test_set_dataframe[i] > 0).astype('int64')
    
    
#     print('----------------------------------------')
#     accuracy_score = sklearn.metrics.accuracy_score(test_, predict_)
#     print('accuracy_score for {} is {}'.format(i,accuracy_score))
#     classification_report = sklearn.metrics.classification_report(test_, predict_)
#     print('classification_report for {} is following'.format(i))
#     print(classification_report)
#     confusion_matrix = sklearn.metrics.confusion_matrix(test_, predict_)
#     print('accuracy_score for {} is following'.format(i))
#     print(confusion_matrix)
    


# # 和训练集重复， T = 10

# train_for_predict_dataset = training_rolling_data[-100:]

# predict_set = []
# index_set = []
# minimal_score_set = []

# for i in range(len(test_rolling_data)):
    
#     train_data_epochs = train_for_predict_dataset[-100:]
   
#     model_p = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                         startprob_prior = initial_start_prob,
#                         transmat_prior = initial_transmat,
#                         means_prior = initial_means,
#                         covars_prior = initial_covars,
#                         init_params = ' ' ).fit(train_data_epochs)
    

    
#     while model_p.transmat_.sum() != 3:
    
#         model_p = GaussianHMM(n_components=3, n_iter=1000,covariance_type = 'full',
#                     startprob_prior = initial_start_prob,
#                     transmat_prior = initial_transmat,
#                     means_prior = initial_means,
#                     covars_prior = initial_covars,
#                     init_params = ' ' ).fit(train_data_epochs)
        
    
    
#     initial_start_prob = model_p.startprob_
#     initial_transmat = model_p.transmat_
#     initial_means = model_p.means_
#     initial_covars = model_p.covars_
    

#     current_score = model_p.score(train_data_epochs[-5:])

#     predict_next_day, index, minimal_score = rolling_compare(current_score,history_sequences,model_p)

#     train_for_predict_dataset = np.r_[train_for_predict_dataset,[predict_next_day]]
    

#     predict_set.append(predict_next_day)

#     index_set.append(index)

#     minimal_score_set.append(minimal_score)
    
  
# predict_set_array = np.array(predict_set) 
    
# '''--------------metrics--------------'''


# import sklearn
# #
# predict_set_dataframe = pd.DataFrame(predict_set_array, columns = [1,2,3,4,5,6])

# test_set_dataframe = pd.DataFrame(test_rolling_data, columns = [1,2,3,4,5,6])

# for i in range(1,7):
    
#     # transform to 0/1
#     predict_ = (predict_set_dataframe[i] > 0).astype('int64')
#     test_ = (test_set_dataframe[i] > 0).astype('int64')
    
    
#     print('----------------------------------------')
#     accuracy_score = sklearn.metrics.accuracy_score(test_, predict_)
#     print('accuracy_score for {} is {}'.format(i,accuracy_score))
#     classification_report = sklearn.metrics.classification_report(test_, predict_)
#     print('classification_report for {} is following'.format(i))
#     print(classification_report)
#     confusion_matrix = sklearn.metrics.confusion_matrix(test_, predict_)
#     print('accuracy_score for {} is following'.format(i))
#     print(confusion_matrix)



    
    # # predict
    # for i in range(len(train_data)):
        
    #     current_score = model.score(initial_sequences)
        
    #     predict_next_day, index, minimal_score = rolling_compare(current_score,train_data,model)
        
    #     initial_sequences = np.r_[initial_sequences,[predict_next_day]]
        
    #     initial_sequences = initial_sequences[-100:]
        
    #     predict_set.append(predict_next_day)
    
    #     index_set.append(index)
    
    #     minimal_score_set.append(minimal_score)
        
    #     i_set.append(begin_index - 100 + i)
    
    
    # predict_set_array = np.array(predict_set)
        
    
    
    
    
    



































