#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:39:59 2020

@author: Roy
"""
import tushare as ts
import datetime
import pandas as pd 
import time
# setup tushare token    
ts.set_token('ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592')

ts_pro = ts.pro_api()
fund_basic = ts_pro.fund_basic(market = 'O',status = 'L')

mixture_fund_basic = fund_basic[fund_basic['fund_type'] == '混合型']

mixture_fund_basic_list = list(mixture_fund_basic['ts_code'])


fund_manager = pd.DataFrame()
i = 0
for tick in mixture_fund_basic_list:
    print(i)
    i += 1
    temp = ts_pro.fund_manager(ts_code = tick)
    fund_manager =  pd.concat([fund_manager, temp], ignore_index=True)
    time.sleep(0.1)
    

fund_manager['end_date'] = fund_manager['end_date'].fillna(datetime.date.today())




fund_manager['end_date'] = pd.to_datetime(fund_manager['end_date'])
fund_manager['begin_date'] = pd.to_datetime(fund_manager['begin_date'])

fund_manager['Days'] =  fund_manager['end_date'] - fund_manager['begin_date']
fund_manager['Days'] = fund_manager['Days'].apply(lambda x: x.days)

selected_fund_manager = fund_manager[fund_manager['Days'] > 1000]

selected_fund_manager = selected_fund_manager[selected_fund_manager['end_date'].apply(lambda x: x.strftime('%Y-%m-%d')) == datetime.date.today().strftime('%Y-%m-%d')]

selected_fund_manager_dd = selected_fund_manager.drop_duplicates(subset = ('name','end_date','resume'))

selected_fund_manager_dd.to_csv(r'D:\RoyMa\Python\Investment\lab\FoF\code\manager_analysis\fund_list.csv', index = False)










