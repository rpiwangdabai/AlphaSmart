#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 23:57:41 2020

@author: Roy
"""

import tushare as ts 
import pandas as pd
import math

# set up token
ts.set_token('260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c')
ts_pro = ts.pro_api()

# # get data
# df = ts_pro.fund_nav(ts_code = '519688.OF')
# fund list
fund_data = ts_pro.fund_basic(market='O')

# choice fund type
fund_data_choosen = fund_data.loc[fund_data['fund_type'].isin(['股票型','混合型'])]

# choice fund type 
fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['type'].isin(['契约型开放式'])]

# # choice fund found date 1603——1803
# fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] > '20160301']
# fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] < '20180301']

# choice fund found date before 14-3
fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] < '20140301']

# choice status
fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['status'] == 'L' ]


# df = ts_pro.fund_nav(ts_code='000527.OF')

