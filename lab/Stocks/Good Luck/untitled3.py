#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 18:56:33 2020

@author: Roy
"""

import numpy as np
import pandas as pd
import logging
from sqlalchemy import create_engine
from multiprocessing import cpu_count
from multiprocessing import Pool
import time
import os
import math
from random import shuffle


def data_concat(core_index):
    # set parameters
    forward_period = 5
    dec_pct = 0.05
    inc_pct = 0.1
    #
    
    
    engine_cstock_daily_price_qfq_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_price_daily_qfq' 
    engine_daily_price = create_engine(engine_cstock_daily_price_qfq_address, encoding ='utf8') 
    
    
    conn = create_engine(engine_cstock_daily_price_qfq_address, encoding ='utf8')
    cur = conn.execute('''SHOW TABLES''')
    tables_name = cur.fetchall()
    shuffle(tables_name)
    # tables_name = tables_name[:100]
    
    #
    price_all = pd.DataFrame()
    
    
    # core number
    core_number = cpu_count()
    start = int((core_index - 1) * math.ceil(len(tables_name) / core_number))
    end = int(core_index * math.ceil(len(tables_name) / core_number))
    
    # merge all data with the same column
    t = 0
    for table in tables_name[start:end]:
        print(t)
        t += 1
        table = table[0]
        sql_cmd_price = "SELECT * FROM `" + table + '`;'
        try:
            # daily price data 
            daily_price = pd.read_sql(sql = sql_cmd_price, con = engine_daily_price)
            daily_price = daily_price[::-1]
            daily_price = daily_price.dropna()
        except BaseException:
            continue
            
        if len(daily_price) < 10:
            continue
        # list for saving triple barrier labels
        label = []
        
        for i in range(len(daily_price)-forward_period):
            date_price = daily_price.iloc[i]['close']
            target_price = [date_price * (1 - dec_pct ), date_price * (1 + inc_pct)]
            flag = False
            for j in range(1,forward_period + 1):
                if daily_price.iloc[i + j]['low'] <= target_price[0]:
                    label.append(0)
                    flag = True
                    break
                elif daily_price.iloc[i + j]['high'] >= target_price[1]:
                    label.append(1)
                    flag = True
                    break
            if flag:
                continue
                
            period_ret = daily_price.iloc[i + j]['close'] / date_price - 1
            label.append(period_ret)
        
        
        placeholder = [np.nan] * forward_period
        label = label + placeholder
        daily_price['label'] = label
        daily_price = daily_price.dropna()
    
        price_all = pd.concat([price_all, daily_price])
    
    return price_all




# =============================================================================
# multiprocessing       
# =============================================================================
core_index = cpu_count()
p = Pool(core_index)  
results = []
for i in range(1, core_index + 1): 
    results.append(p.apply_async(data_concat, args=(i,)))
print ('等待所有子进程结束...')
p.close()
p.join()
print ('所有子进程结束...')


# =============================================================================
# merge
# =============================================================================
price_all = pd.DataFrame()
for i in range(len(results)):
    price = results[8].get()
    price_all = pd.concat([price_all, price])


price_all.to_csv('/Users/Roy/Desktop/price_lab.csv')

# engine_test_lab_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/lab_test' 
# engine_test_lab = create_engine(engine_test_lab_address, encoding ='utf8') 
# pd.io.sql.to_sql(price_all, 'price_with_lab', engine_test_lab ,index = None,if_exists = 'replace') ## change


