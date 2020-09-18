# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 18:56:46 2020

@author: Lenovo
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine

data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow'
conn = create_engine(data_base_address, encoding ='utf8')
cur = conn.execute('''SHOW TABLES''')
tables_name = cur.fetchall()






conn =  pymysql.connect(host = 'localhost', user = 'root', password = 'ai3ilove', 
                  db = 'stock_daily_capital_flow', port = 3306, charset = 'utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = '''SHOW TABLES'''
        cursor.execute(sql)
        tables_name = cursor.fetchall()
finally:
    conn.close
    


# get table column names 
sql_cmd = "SELECT * FROM `" + tables_name[0][0] + '`;'
daily_price = pd.read_sql(sql = sql_cmd, con = conn)
temp_data = pd.read_sql(sql = sql_cmd, con = conn)
columns = temp_data.columns[2:]

# build column dataframe
for column in columns:
    script = column + '=pd.DataFrame()' 
    exec(script)


i = 0
for name in tables_name[:10]:
    i += 1
    print(i)
    name = name[0]
    sql_cmd = "SELECT * FROM `" + name + '`;'
    daily_price = pd.read_sql(sql = sql_cmd, con = conn)
    
    for column in columns:
        
    
        target_data = daily_price[['trade_date',column]]
        column_name = column + '_' + name
        target_data = target_data.rename(columns = {column : column_name})
        merge_script = """
if len( """+ column + """) == 0:
    """+ column + """ = target_data.copy()
else:
    """+ column + """ = pd.merge("""+ column + """,target_data,on = 'trade_date', how = 'outer')
"""
                
        exec(merge_script)



for column in columns:
    
    saving_script = "pd.io.sql.to_sql(" + column + ", str.lower(tick), conn,index = None,if_exists = 'replace')"
    exec(script)     
    
    
    
    
    

    
    
    
    
     try:
                pd.io.sql.to_sql(data, str.lower(tick), self.conn,index = None,if_exists = 'replace') ## change
            except ValueError:
                error_ticks.append(tick)
    
    
    
    
    
    
    
    
    

