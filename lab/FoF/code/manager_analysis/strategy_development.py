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
    fund_data = fund_data[fund_data['end_date'] < '20200101']
    fund_data = fund_data.drop_duplicates(subset = ['end_date'])

    if i == 0:
        portfolio_adj_nav = fund_data[['end_date','adj_nav']].copy()
        portfolio_adj_nav = portfolio_adj_nav.rename(columns = {'adj_nav':tick})
    else:
        portfolio_adj_nav = pd.merge(portfolio_adj_nav,fund_data[['end_date','adj_nav']],how = 'inner')
        portfolio_adj_nav = portfolio_adj_nav.rename(columns = {'adj_nav':tick})
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



# =============================================================================
# K-means
# =============================================================================
from sklearn.cluster import KMeans
from sklearn import metrics  
# tansfer 
K = [i for i in range(2,10)]
portfolio_adj_nav_t = portfolio_adj_nav.T
ch_index = []
sc = []
SSE = []
for k in K:
    estimator = KMeans(n_clusters = k).fit(portfolio_adj_nav_t)
    y_pred  = estimator.predict(portfolio_adj_nav_t)
    # ch_index.append(metrics.calinski_harabasz_score(portfolio_adj_nav_t, y_pred))
    sc.append(metrics.silhouette_score(portfolio_adj_nav_t, y_pred,metric='euclidean'))
    # SSE.append(estimator.inertia_)
# plt.plot(K,ch_index,'s-',color = 'r', label='ch-index')
plt.plot(K,sc,'o-',color = 'g', label='sc')
# plt.plot(K,SSE,'o-',color = 'g', label='sc')
plt.legend(loc = "best")
plt.show()

# =============================================================================
#  reset plot corr heatmap
# =============================================================================
k = 4
estimator = KMeans(n_clusters = k).fit(portfolio_adj_nav_t)
y_pred  = estimator.predict(portfolio_adj_nav_t)
# fund list
fund_list = list(portfolio_adj_nav_t.index)
fund_cluster = pd.DataFrame()
fund_cluster['fund_ticks'] = fund_list
fund_cluster['cluster'] = y_pred 
fund_cluster = fund_cluster.sort_values(by='cluster')
sorted_list = fund_cluster['fund_ticks']
portfolio_adj_nav_cluster = portfolio_adj_nav[sorted_list]

#sublists
portfolio_adj_nav_sub_list = list(fund_cluster[fund_cluster['cluster'] == 0]['fund_ticks'])

# plot corr heatmap
portfolio_adj_nav_sub = portfolio_adj_nav[portfolio_adj_nav_sub_list]
plt.figure(figsize=(40,40))
plt.title('Pearson Correlation of Features',y=1.05,size=45)
sns.heatmap(portfolio_adj_nav_sub.astype(float).corr(),linewidths=0.1,vmax=1.0,
            square=True,linecolor='white',annot=True)
plt.show()

# =============================================================================
# cluster cor check
# =============================================================================

portfolio_adj_nav_t['cluster'] = y_pred
result = portfolio_adj_nav_t.groupby('cluster').mean()


plt.figure(figsize=(40,40))
plt.title('Pearson Correlation of Features',y=1.05,size=45)
sns.heatmap(result.T.astype(float).corr(),linewidths=0.1,vmax=1.0,
            square=True,linecolor='white',annot=True)
plt.show()






