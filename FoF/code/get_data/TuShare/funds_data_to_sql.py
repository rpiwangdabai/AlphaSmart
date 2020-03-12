#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 22:35:54 2020

@author: Roy
"""

''''
Download data through tushare and save the fund data to sql
'''

import tushare as ts 
import pandas as pd
from sqlalchemy import create_engine
import time

'''-----------set up-----------'''
# set token
ts.set_token('260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c')
ts_pro = ts.pro_api()

# connect to database


# build connect
conn = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

'''-----------download fund data and save to sql-----------'''
#load data ticks     
funds_data = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/Tushare/fundcode_before1603_1803.csv')
fund_tick = list(funds_data['ts_code'])

# id count
i = 1
# get fund data and save it to sql
while fund_tick:
    print(i)
    i += 1 
    ticks = fund_tick.pop()
    data = ts_pro.fund_nav(ts_code=ticks)
    time.sleep(0.3)
    # save data to sql
    try:
        pd.io.sql.to_sql(data, ticks, conn,index = None)
    except ValueError:
        continue
    










