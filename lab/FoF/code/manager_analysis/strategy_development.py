#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:45:16 2020

@author: Roy
"""
import pandas as pd 
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import pandas as pd
import math
import collections
import matplotlib.patches as mpatches
from mlfinlab.portfolio_optimization.clustering import HierarchicalEqualRiskContribution

from mlfinlab.portfolio_optimization.clustering import HierarchicalRiskParity
# =============================================================================
# import data
# =============================================================================
selected_data_2 = pd.read_csv('D:/RoyMa/Python/Investment/lab/FoF/code/manager_analysis/select_method_2/selected_fund_by_sharp.csv')



'''-----------get fund data and calculate correlation with index-----------'''
# get funds ticks
engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')
ticks = collections.deque(selected_data_2['Ticks'])

i = 0
portfolio_adj_nav = pd.DataFrame()
while ticks:
    #get fund data by ticks
    tick = ticks.popleft()
    sql_cmd = "SELECT * FROM `" + tick + '`;'
    fund_data = pd.read_sql(sql=sql_cmd, con=engine)
    fund_init_date = fund_data.iloc[-1]['end_date']
    if i == 0:
        portfolio_adj_nav['end_date'] = fund_data['end_date']
        portfolio_adj_nav[tick] = fund_data['adj_nav']
        closest_date = fund_init_date
    else:
        if fund_init_date >= closest_date:
            closest_date = fund_init_date
            portfolio_adj_nav = portfolio_adj_nav[portfolio_adj_nav['end_date']
                                                  > closest_date]
            portfolio_adj_nav[tick] = fund_data['adj_nav']
        else:
            portfolio_adj_nav[tick] = fund_data[fund_data['end_date'] > closest_date]['adj_nav']
    i += 1
    print(i)

# size = portfolio_adj_nav.shape[0]
# drop_row = [i for i in range(size-40,size)]
# portfolio_adj_nav = portfolio_adj_nav.drop(drop_row)

portfolio_adj_nav['end_date'] = pd.to_datetime(portfolio_adj_nav['end_date'])
portfolio_adj_nav = portfolio_adj_nav.set_index('end_date')
portfolio_adj_nav = portfolio_adj_nav.dropna()
    




# =============================================================================
#  colculation weights
# =============================================================================
herc = HierarchicalEqualRiskContribution()
herc.allocate(asset_names=portfolio_adj_nav.columns, 
              asset_prices=portfolio_adj_nav, 
              risk_measure = 'standard_deviation',
              linkage="ward")
# plotting our optimal portfolio
herc_weights = herc.weights
y_pos = np.arange(len(herc_weights.columns))
plt.figure(figsize=(25,7))
plt.bar(list(herc_weights.columns), herc_weights.values[0])
plt.xticks(y_pos, rotation=45, size=10)
plt.xlabel('Assets', size=20)
plt.ylabel('Asset Weights', size=20)
plt.title('HERC Portfolio Weights', size=20)
plt.show()


plt.figure(figsize=(30,17))
herc.plot_clusters(assets=portfolio_adj_nav.columns)
plt.title('HERC Dendrogram', size=18)
plt.xticks(rotation=45)
plt.show()




hrp = HierarchicalRiskParity()
hrp.allocate(asset_prices=portfolio_adj_nav)

# Plot Dendrogram
hrp.plot_clusters(assets=portfolio_adj_nav.columns)




# =============================================================================
# plot corr heatmap
# =============================================================================
plt.figure(figsize=(40,40))
plt.title('Pearson Correlation of Features',y=1.05,size=45)
sns.heatmap(portfolio_adj_nav.astype(float).corr(),linewidths=0.1,vmax=1.0,
            square=True,linecolor='white',annot=True)
plt.show()

