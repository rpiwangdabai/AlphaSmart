#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 02:47:46 2020

@author: Roy
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tushare as ts
import scipy.optimize as sco
import scipy.interpolate as sci
from scipy import stats

df = pd.DataFrame()

# stocks = ['000651.SZ',       ##格力电器   
#           '600519.SH',       ##贵州茅台  
#           '601318.SH',       ##中国平安               
#           '000858.SZ',       ##五粮液  
#           '600887.SH',       ##伊利股份  
#           '000333.SZ',       ##美的集团   
#           '601166.SH',       ##兴业银行  
#           '600036.SH',       ##招商银行  
#           '601328.SH',       ##交通银行  
#           '600104.SH'        ##上汽集团
#           ]


ts.set_token('260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c')
ts = ts.pro_api()

data1 = ts.daily(ts_code = stocks[0], start='2016-05-28', end='2017-05-26')
data2 = ts.daily(ts_code = stocks[1], start='2016-05-28', end='2017-05-26')
data3 = ts.daily(ts_code = stocks[2], start='2016-05-28', end='2017-05-26')
data4 = ts.daily(ts_code = stocks[3], start='2016-05-28', end='2017-05-26')
data5 = ts.daily(ts_code = stocks[4], start='2016-05-28', end='2017-05-26')
data6 = ts.daily(ts_code = stocks[5], start='2016-05-28', end='2017-05-26')
data7 = ts.daily(ts_code = stocks[6], start='2016-05-28', end='2017-05-26')
data8 = ts.daily(ts_code = stocks[7], start='2016-05-28', end='2017-05-26')
data9 = ts.daily(ts_code = stocks[8], start='2016-05-28', end='2017-05-26')
data10 = ts.daily(ts_code = stocks[9], start='2016-05-28', end='2017-05-26')



data = pd.concat([data1['close'],data2['close'],data3['close'],data4['close'],
              data5['close'],data6['close'],data7['close'],data8['close'],
              data9['close'],data10['close']],axis=1)

data.columns = stocks
data = data.dropna()

print(data.info())

# cal log return 
log_returns = np.log(data / data.shift(-1))

#
rets = log_returns
# annuality
year_ret = rets.mean() * 252
# cov
year_volatility = rets.cov() * 252

#
number_of_assets = 10
# 10 random number
weights = np.random.random(number_of_assets)
# normalization
weights /= np.sum(weights)

portfolio_returns = []
portfolio_volatilities = []
for p in range (5000):
    weights = np.random.random(number_of_assets)
    weights /= np.sum(weights)
    portfolio_returns.append(np.sum(rets.mean() * weights) * 252)
    portfolio_volatilities.append(np.sqrt(np.dot(weights.T, 
                      np.dot(rets.cov() * 252, weights))))
    
portfolio_returns = np.array(portfolio_returns)
portfolio_volatilities = np.array(portfolio_volatilities)

plt.figure(figsize=(9, 5)) #作图大小
plt.scatter(portfolio_volatilities, portfolio_returns, c=portfolio_returns / portfolio_volatilities, marker='o') #画散点图
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')



#
def statistics(weights):
    weights = np.array(weights)
    pret = np.sum(rets.mean() * weights) * 252
    pvol = np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights)))
    return np.array([pret, pvol, pret / pvol])


def min_func_sharpe(weights):
    return -statistics(weights)[2]

def min_func_variance(weights):
    return statistics(weights)[1] ** 2

bnds = tuple((0,1) for x in range(number_of_assets))
cons = ({'type' : 'eq', 'fun' : lambda x: np.sum(x) - 1})

opts = sco.minimize(min_func_sharpe, 
                    number_of_assets * [1. / number_of_assets],
                    method = 'SLSQP', 
                    bounds = bnds,
                    constraints = cons)

optv = sco.minimize(min_func_variance, 
                    number_of_assets * [1. / number_of_assets,],
                    method = 'SLSQP', 
                    bounds = bnds,
                    constraints = cons)


def min_func_port(weights):
    return statistics(weights)[1] 

target_returns = np.linspace(0.01, 0.30, 30)

target_volatilities = []

for tret in target_returns:
    cons = ({'type': 'eq', 'fun': lambda x:  statistics(x)[0] - tret},
            {'type': 'eq', 'fun': lambda x:  np.sum(x) - 1})
    res = sco.minimize(min_func_port, number_of_assets * [1. / number_of_assets,], method='SLSQP',
                       bounds=bnds, constraints=cons)
    target_volatilities.append(res['fun'])
    
#画散点图
plt.figure(figsize=(9, 5))
#圆点为随机资产组合
plt.scatter(portfolio_volatilities, portfolio_returns,
            c=portfolio_returns / portfolio_volatilities, marker='o')
#叉叉为有效边界            
plt.scatter(target_volatilities, target_returns,
            c=target_returns / target_volatilities, marker='x')
#红星为夏普率最大值的资产组合            
plt.plot(statistics(opts['x'])[1], statistics(opts['x'])[0],
         'r*', markersize=15.0)
#黄星为最小方差的资产组合            
plt.plot(statistics(optv['x'])[1], statistics(optv['x'])[0],
         'y*', markersize=15.0)
            # minimum variance portfolio
plt.grid(True)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')



ind = np.argmin(target_volatilities)

upper_half_volatilities = target_volatilities[ind:]
upper_half_returns = target_returns[ind:]

tck = sci.splrep(upper_half_volatilities, upper_half_returns)
#tck参数用于构造有效边界函数f(x)
def f(x):
    #有效边界函数 (样条函数逼近).
    return sci.splev(x, tck, der=0)

#同时也构造有效边界函数f(x)的一阶导数函数df(x)
def df(x):
    #有效边界函数f(x)的一阶导数函数 
    return sci.splev(x, tck, der=1)

def equations(p, risk_free_return=0.02):
    eq1 = risk_free_return - p[0]
    eq2 = risk_free_return + p[1] * p[2] - f(p[2])
    eq3 = p[1] - df(p[2])
    return eq1, eq2, eq3


opt = sco.fsolve(equations, [0.01, 0.50, 0.15])



#圆点为随机资产组合
plt.scatter(portfolio_volatilities, portfolio_returns,
            c=(portfolio_returns - 0.02) / portfolio_volatilities, marker='o')
#绿色线为有效边界
plt.plot(upper_half_volatilities, upper_half_returns, 'g', lw=4.0)

#设定资本市场线CML的x范围从0到0.6           
cml_x = np.linspace(0.0, 0.6)
#带入公式a+b*x求得y,作图
plt.plot(cml_x, opt[0] + opt[1] * cml_x, lw=1.5)
#标出资本市场线与有效边界的切点，红星处            
plt.plot(opt[2], f(opt[2]), 'r*', markersize=15.0) 
plt.grid(True)
plt.axhline(0, color='k', ls='--', lw=2.0)
plt.axvline(0, color='k', ls='--', lw=2.0)
plt.xlabel('expected volatility')
plt.ylabel('expected return')
plt.colorbar(label='Sharpe ratio')

