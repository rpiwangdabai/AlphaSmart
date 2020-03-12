#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 21:01:56 2020

@author: Roy
"""

import pymysql
import pandas as pd
from sqlalchemy import create_engine

# build connect
conn = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/fund', 
                     encoding ='utf8')
#test pd
data = pd.DataFrame([1,2,3],columns = ['A'])

#save dataframe to sql 
pd.io.sql.to_sql(data, 'test', conn,index = None)

