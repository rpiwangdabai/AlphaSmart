# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 07:35:59 2020

@author: mazhu
"""

import tushare as ts 
import numpy as np
import pandas as pd 

token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'

# setup tushare token        
ts.set_token(token)
ts_pro = ts.pro_api()
tick = '000001.SZ'


data_price  = ts.pro_bar(ts_code=tick, adj = 'hfq')


data_basic = ts_pro.daily_basic(ts_code=tick)

data_money_flow = ts_pro.moneyflow(ts_code=tick)




data_price['trade_date'] = pd.to_datetime(data_price['trade_date'])
data_price.set_index('trade_date',inplace=True)


data_basic['trade_date'] = pd.to_datetime(data_basic['trade_date'])
data_basic.set_index('trade_date', inplace = True)

data_money_flow['trade_date'] = pd.to_datetime(data_money_flow['trade_date'])
data_money_flow.set_index('trade_date', inplace = True)


test = data_money_flow.join(data_basic, how = 'inner')

pd.merge(data_money_flow,data_basic,how = 'inner')
