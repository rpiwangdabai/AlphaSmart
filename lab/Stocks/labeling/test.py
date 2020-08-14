# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:08:43 2020

@author: Lenovo
"""

# =============================================================================
# increase barrier
# decrease barrier
# time period barrier 
# =============================================================================

import tushare as ts 
import numpy as np
import pandas as pd 

token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'

# setup tushare token        
ts.set_token(token)
ts_pro = ts.pro_api()

data = ts.pro_bar(ts_code='000001.SZ', adj = 'hfq')

'''---triple barrier function---'''
data_ = data.dropna()
data_ = data_.iloc[::-1]


label = []

inc_pct = 0.1
dec_pct = 0.05
period = 5

for i in range(len(data_)-5):
    date_price = data_.iloc[i]['close']
    target_price = [date_price * (1 - dec_pct ), date_price * (1 + inc_pct)]
    
    flag = False
    
    for j in range(1,6):
        if data_.iloc[i + j]['low'] <= target_price[0]:
            print(i)
            label.append(0)
            flag = True
            break
        elif data_.iloc[i + j]['high'] >= target_price[1]:
            label.append(1)
            flag = True
            break
    
    if flag:
        continue
        
    period_ret = data_.iloc[i + j]['close'] / date_price - 1
    label.append(period_ret)


placeholder = [np.nan] * period
label = label + placeholder
data_['label'] = label
        
        
        
        






