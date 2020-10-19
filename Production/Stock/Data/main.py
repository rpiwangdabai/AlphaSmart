# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 15:18:17 2020

@author: Lenovo
"""

from listed_stock_data.listed_data import ListedData
from individual_stock_data.basic.stock_daily_basic import StockDailyBasic
from individual_stock_data.capitalflow.stock_daily_capital_flow import StockDailyCapitalFlow
from individual_stock_data.price.stock_daily_price import StockDailyPrice


'''------set up token------'''
# set token
token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'
log_file_name = 'daily_log.log'

# =============================================================================
# listed stock list update
# =============================================================================
'''------Listed stock list------'''
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
'''-----------download listed stock ticks info  and save to sql-----------'''
ld = ListedData(token, data_base_address, log_file_name)
ld.run()  

# =============================================================================
# stock daily basic info update
# =============================================================================
'''------stock daily basic------'''
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
'''-----------download stock data and save to sql-----------'''
s_d_b = StockDailyBasic(token, data_base_address,log_file_name)
s_d_b.run()

# =============================================================================
# stock daily capital flow update
# =============================================================================
'''------stock daily capital flow update------'''
# set data_base_address
stock_ticks_data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_capital_flow'
'''-----------download stock capital flow data and save to sql-----------'''
s_d_b = StockDailyCapitalFlow(token, data_base_address,stock_ticks_data_base_address,log_file_name)
s_d_b.run()

# =============================================================================
# stock daily price update 
# =============================================================================
'''------None-----'''

'''------stock daily price update------'''
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_price_none'
stock_ticks_data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
'''-----------download stock data and save to sql-----------'''
s_d_b = StockDailyPrice(token, data_base_address,stock_ticks_data_base_address,log_file_name)
s_d_b.run('None')

'''------qfq-----'''

'''------stock daily price update------'''
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_price_qfq'
stock_ticks_data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
'''-----------download stock data and save to sql-----------'''
s_d_b = StockDailyPrice(token, data_base_address,stock_ticks_data_base_address,log_file_name)
s_d_b.run('qfq')

'''------hfq-----'''

'''------stock daily price update------'''
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_price_hfq'
stock_ticks_data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
'''-----------download stock data and save to sql-----------'''
s_d_b = StockDailyPrice(token, data_base_address,stock_ticks_data_base_address,log_file_name)
s_d_b.run('hfq')
    


