# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 18:56:46 2020

@author: Lenovo
"""

import datetime
import numpy as np
from matplotlib import cm, pyplot as plt
import matplotlib.dates as dates
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine

import pymysql

conn =  pymysql.connect(host = 'localhost', user = 'root', password = 'ai3ilove', 
                  db = 'stock_daily_capital_flow', port = 3306, charset = 'utf8mb4')

cursor = conn.cursor()
data = cursor.execute('SELECT buy_sm_vol FROM `000001.sz` WHERE trade_date = 20200826')
one = cursor.fetchone()[0]

new = dict(zip([x[0] for x in cursor.description],[x for x in cursor.fetchone()]))

if conn:
    conn.close()


def new2dict(new):
 return dict(zip([x[0] for x in cursor.description],[x for x in new]))
news_list = list(map(new2dict,cursor.fetchall()))

'''------traverse------'''

conn =  pymysql.connect(host = 'localhost', user = 'root', password = 'ai3ilove', 
                  db = 'stock_daily_capital_flow', port = 3306, charset = 'utf8mb4')

tables_name = []

try:
    with conn.cursor() as cursor:
        sql = '''SHOW TABLES'''
        cursor.execute(sql)
        tables_name = cursor.fetchall()
finally:
    conn.close
    


result_merge = pd.DataFrame()

i = 0
for name in tables_name:
    i += 1
    print(i)
    name = name[0]
    sql_cmd = "SELECT * FROM `" + name + '`;'
    daily_price = pd.read_sql(sql = sql_cmd, con = conn)
    
    target_data = daily_price[['trade_date','buy_sm_vol']]
    column_name = 'buy_sm_vol_' + name
    target_data = target_data.rename(columns = {'buy_sm_vol' : 'buy_sm_vol_000002'})
    if len(result_merge) == 0:
        result_merge = target_data.copy()
    else:
        result_merge = pd.merge(result_merge,target_data,on = 'trade_date', how = 'outer')





        sql_cmd = "SELECT * FROM `" + '000001.sz' + '`;'
        daily_price = pd.read_sql(sql = sql_cmd, con = conn)



df.rename(columns={"A": "a", "B": "c"})



sql_cmd = "SELECT * FROM `" + '000001.sz_hfq' + '`;'

    
    


