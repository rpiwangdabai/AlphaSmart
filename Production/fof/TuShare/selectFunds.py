#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 23:57:41 2020

@author: Roy
"""

import tushare as ts 
import pandas as pd
import math
import sys
sys.path.append('.')
from Config.userConfig import TS_TOKEN
# set up token
ts.set_token(TS_TOKEN)
tsPro = ts.pro_api()

# # get data
# df = ts_pro.fund_nav(ts_code = '519688.OF')
# fund list
#ETF
etfData = tsPro.fund_basic(market='E')
# out of market
lofData = tsPro.fund_basic(market='O')
# choice fund type all
#fundDataChoosen = fundData.loc[fundData['fund_type'].isin(['股票型','混合型','债券型'])]

fundData = pd.concat([etfData, lofData], axis = 0)
# choice fund type 
fundDataChoosen = fundData.loc[fundData['type'].isin(['契约型开放式'])]

# # choice fund found date 1603——1803
# fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] > '20160301']
# fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] < '20180301']

# choice fund found date before 14-3
fundDataChoosen = fundDataChoosen.loc[fundDataChoosen['found_date'] < '20140301']
# choice status: issued
fundDataChoosen = fundDataChoosen.loc[fundDataChoosen['status'] == 'L' ]


