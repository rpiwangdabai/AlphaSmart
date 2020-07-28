# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Tue Jul 14 14:20:17 2020

# @author: Roy
# """

import tushare as ts 
import pandas as pd
import numpy as np
import logging
from sqlalchemy import create_engine
import time

token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'

ts.set_token(token)
ts_pro = ts.pro_api()

# data = ts_pro.daily_basic(ts_code='000001.SZ')



# ts.set_token(token)

# df_qfq = ts.pro_bar(ts_code='000001.SZ', adj='qfq', freq = 'D',start_date='20180101', end_date='20181011')

# df_hfq = ts.pro_bar(ts_code='000001.SZ', adj='hfq', freq = 'D',start_date='20180101', end_date='20181011')

df_None = ts.pro_bar(ts_code='002149.SZ', adj='None', freq = 'D')

df = ts_pro.moneyflow(ts_code='002149.SZ')


# engine_mv = create_engine('mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic', 
#                      encoding ='utf8')

# sql_cmd = "SELECT * FROM `liseted stock list`;"
# stock_data = pd.read_sql(sql=sql_cmd, con=engine_mv)


# import logging

# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='myapp.log',
#                 filemode='a')
    
# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')



































