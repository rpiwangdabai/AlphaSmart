#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:07:21 2020

@author: Roy
"""
# %pylab
# %matplotlib inline
# pylab.rcParams['figure.figsize'] = (10, 6)
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import scipy
import math
import collections


# Calculate portfolio mean return
def port_mean(W,R):
    return sum(R * W)

# Calculate portfolio variance of returns
def port_var(W,C):
    return np.dot(np.dot(W, C), W)

# Combination of the two functions above - mean and variance of returns calculation
def port_mean_var(W, R ,C):
    return port_mean(W,R), port_var(W,C)


# Given risk - free rate, assets returns and covariances, this function calculates
# weights of tangency portfolio with respect to sharp ratio maxmization

def solve_weights(R, C, rf):
    
    def fitness(W, R, C, rf):
        mean, var = port_mean_var(W, R, C)
        # utillity = Sharp ratio
        util = (mean - rf) / math.sqrt(var)
        # maxmize the utility, minimize its inverse value
        return -util
        
    n = len(R)
    W = np.ones([n]) / n
    b_ = [(0., 1.) for i in range(n)]
    c_ = {'type' : 'eq', 'fun' : lambda W : sum(W) - 1.} 
    optimized = scipy.optimize.minimize(fitness, W, (R,C,rf),
                                        method = 'SLSQP',
                                        constraints = c_,
                                        bounds = b_)
    if not optimized.success:
        raise BaseException(optimized.message)
    return optimized.x


''''---------load data---------'''
# load seleted fund data ticks
data = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/Fund correlation/selcted_fund.csv')
ticks = collections.deque(data['Ticks'])
data_weight = np.array(data['规模'])
# load data from sql database
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')
data_log_ret = pd.DataFrame()

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
portfolio_log_ret = portfolio_log_ret.drop(['end_date'], axis = 1)
    
    
    
    
    
    # tick = ticks.popleft()
    # sql_cmd = "SELECT * FROM `" + tick + '`;'
    # fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    # data_log_ret[tick] = fund_data['log_ret']
    


data_log_ret = portfolio_log_ret.copy()


    
      
W = data_weight / sum(data_weight)
R = data_log_ret.mean() * 252 # annualize
C = data_log_ret.cov() * 252 # annualized
rf = 0.0344 # risk free rate (log) +3.5%
tau = 0.025

# veiw
# P = np.zeros([1,13])
# # view 1 : stock base have 10% return more than the rest 
# P[0][0] = -0.25
# P[0][1] = -0.25
# P[0][2] = -0.25
# P[0][3] = -0.25
# P[0][4] = 1
# P[0][5] = 0
# P[0][6] = 0
# P[0][7] = 0
# P[0][8] = 0
# P[0][9] = 0
# P[0][10] = 0
# P[0][11] = 0
# P[0][12] = 0

# # view 2 : stock base have 10% return more than the rest 
# P[1][0] = -0.25
# P[1][1] = -0.25
# P[1][2] = -0.25
# P[1][3] = -0.25
# P[1][4] = 0
# P[1][5] = 0
# P[1][6] = 0
# P[1][7] = 0
# P[1][8] = 0.2
# P[1][9] = 0.2
# P[1][10] = 0.2
# P[1][11] = 0.2
# P[1][12] = 0.2

P = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/Fund correlation/view.csv',header = None)
P = np.array(P.values)
Q = np.array([0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,1,1])

def blacklitterman(W, R, C, P, Q, tau, rf):
    mean, var = port_mean_var(W, R, C) # portfolio mean and var under equilibrium weights
    
    lmb = (mean - rf) / var # Calculate risk aversion
    Pi = np.dot(np.dot(lmb, C), W) # Calcuate equilibrium excess returns
    
    ts = tau * C
    ts_1 = np.linalg.inv(ts)
    Omega = np.dot(np.dot(P,ts), P.T)* np.eye(Q.shape[0])
    Omega_1 = np.linalg.inv(Omega)
    er = np.dot(np.linalg.inv(ts_1 + np.dot(np.dot(P.T,Omega_1),P)),(np.dot(ts_1 ,Pi)+np.dot(np.dot(P.T,Omega_1),Q)))
    posterirorSigma = np.linalg.inv(ts_1 + np.dot(np.dot(P.T,Omega_1),P)) + C
    
    return [er, posterirorSigma]
        
bl_mean, bl_var = blacklitterman(W, R, C, P, Q, tau, rf)
res =  solve_weights(bl_mean, bl_var, rf)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
