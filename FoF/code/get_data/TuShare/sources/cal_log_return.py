#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 10:44:30 2020

@author: Roy
"""

from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')

#get tables name
tables = engine.table_names()
#get table from database, cal log turn and save it back.
i = 1
while tables:
    name = tables.pop()
    # select table
    sql_cmd = "SELECT * FROM `" + name + '`;'
    data = pd.read_sql(sql=sql_cmd, con=engine)
    # cal log ret
    data['log_ret'] = np.log(data.adj_nav) - np.log(data.adj_nav.shift(-1))
    # save table
    pd.io.sql.to_sql(data, name, engine,index = None,if_exists = 'replace')
    print(i)
    i += 1













