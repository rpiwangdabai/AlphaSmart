# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 09:12:11 2020

@author: Lenovo
"""


import numpy as np
import pandas as pd
import logging
from sqlalchemy import create_engine
from multiprocessing import cpu_count
from multiprocessing import Pool

# =============================================================================
#  samling_merge_dict
# =============================================================================
def sampling_merge(status,data_base_address,filename,core_index):
    
    logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename=filename,
    filemode='a')
    
    # capital flow database address
    engine_capital_flow_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/' + data_base_address['capital_flow']
    engine_capital_flow = create_engine(engine_capital_flow_address, encoding ='utf8')

    # stock daily basic database address
    engine_daily_basic_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/' + data_base_address['daily_basic']
    engine_daily = create_engine(engine_daily_basic_address, encoding ='utf8')

    # stock daily price database address
    engine_daily_price_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/' + data_base_address['daily_price']
    engine_daily_price = create_engine(engine_daily_price_address, encoding ='utf8')

    # stock variabels database address
    engine_stock_variables = 'mysql+pymysql://root:ai3ilove@localhost:3306/' + data_base_address['variable_address_1']
    engine_daily_stock_variabels = create_engine(engine_stock_variables, encoding ='utf8')

    # get all tables = name
    conn = create_engine(engine_capital_flow_address, encoding ='utf8')
    cur = conn.execute('''SHOW TABLES''')
    tables_name = cur.fetchall()
     
    # core number
    core_number = cpu_count()
    start = int((core_index - 1) * round(len(tables_name) / core_number))
    end = int(core_index * round(len(tables_name) / core_number))

    '''-------------'''
    tables_name = tables_name[:24]

    #error ticks list
    error_ticks = []
    # get data and merge by loop
    i = 1
    for table in tables_name[start:end]:
        print(i)
        i += 1
        table = table[0]
        print(table)
        sql_cmd = "SELECT * FROM `" + table + '`;'
        sql_cmd_price = "SELECT * FROM `" + table[:6] + '_' + status + '`;'
        try:
            # capital flow data
            daily_capital_flow = pd.read_sql(sql = sql_cmd, con = engine_capital_flow)
            # daily basic data 
            daily_basic = pd.read_sql(sql = sql_cmd, con = engine_daily)
            # daily price data 
            daily_price = pd.read_sql(sql = sql_cmd_price, con = engine_daily_price)
        except BaseException:
            continue

        # reset index to time index
        daily_capital_flow['trade_date'] = pd.to_datetime(daily_capital_flow['trade_date'])
        daily_capital_flow.set_index('trade_date',inplace=True)
        daily_capital_flow = daily_capital_flow[::-1]
        
        daily_basic['trade_date'] = pd.to_datetime(daily_basic['trade_date'])
        daily_basic.set_index('trade_date',inplace=True)
        daily_basic = daily_basic[::-1]
        
        daily_price['trade_date'] = pd.to_datetime(daily_price['trade_date'])
        daily_price.set_index('trade_date',inplace=True)
        daily_price = daily_price[::-1]
        
        
        del daily_basic['ts_code']
        del daily_price['ts_code']
        data_merge_1 = daily_capital_flow.join(daily_basic)
        data_merge_2 = data_merge_1.join(daily_price, lsuffix='_daily_close_price')
        data_merge_2 = data_merge_2.dropna()


        # list for saving triple barrier labels
        label = []
        
        for i in range(len(data_merge_2)-forward_period):
            date_price = data_merge_2.iloc[i]['close']
            target_price = [date_price * (1 - dec_pct ), date_price * (1 + inc_pct)]
            flag = False
            for j in range(1,forward_period + 1):
                if data_merge_2.iloc[i + j]['low'] <= target_price[0]:
                    label.append(0)
                    flag = True
                    break
                elif data_merge_2.iloc[i + j]['high'] >= target_price[1]:
                    label.append(1)
                    flag = True
                    break
            if flag:
                continue
                
            period_ret = data_merge_2.iloc[i + j]['close'] / date_price - 1
            label.append(period_ret)
        
        
        placeholder = [np.nan] * forward_period
        label = label + placeholder
        data_merge_2['label'] = label
        data_merge_2 = data_merge_2.dropna()


        '''-----------------set variables----------------'''
        a = pd.DataFrame()
        a['columns'] = list(data_merge_2.columns)
        
        data_derivative_variables = pd.DataFrame(index = data_merge_2.index)
        
        set_one_variables = list(data_merge_2.columns)[1:19]
        
        set_two_variables = list(data_merge_2.columns)[20:30]
        
        # set_three_variables = list(data_merge_2.columns)[30:35]
        
        set_four_variables = list(data_merge_2.columns)[35:44]

        
        # =============================================================================
        # '''----set one variables ----'''
        # =============================================================================
        
        '''----set one variables Z value variables----'''
        
        for column in set_one_variables:
            
            column_name = column + '_z_value'
            
            data_derivative_variables[column_name] = (data_merge_2[column] - data_merge_2[column].rolling(window = 5).median()) / data_merge_2[column].rolling(window = 5).std()
        
        '''----set one variables proportion variables----'''

        
        sub_dataset = data_merge_2[set_one_variables[:16]]
        
        data_vol = sub_dataset.iloc[:, [i%2 == 0 for i in range(len(set_one_variables[:16]))]]
        data_amount = sub_dataset.iloc[:, [i%2 == 1 for i in range(len(set_one_variables[:16]))]]
        
        data_vol_proportion = data_vol.div(data_vol.sum(axis=1), axis=0)
        data_amount_proportion = data_amount.div(data_amount.sum(axis=1), axis=0)
        
        #    '''---columns_rename---'''
        col_ratio = []
        for col in data_vol_proportion.columns:
            col_ratio.append(col + '_ratio')
        
        data_vol_proportion.columns = col_ratio
        
        col_ratio = []
        for col in data_amount_proportion.columns:
            col_ratio.append(col + '_ratio')
        
        data_amount_proportion.columns = col_ratio
        
        data_proportion = data_amount_proportion.join(data_vol_proportion)
        
        data_derivative_variables = data_derivative_variables.join(data_proportion)
        
        '''----set one variables proportion Z value variables---- '''
        
        for column in data_proportion.columns:    
            column_name = column + '_z_value'    
            data_derivative_variables[column_name] = (data_proportion[column] - data_proportion[column].rolling(window = 5).median()) / data_proportion[column].rolling(window = 5).std()
        
        
        # =============================================================================
        # '''----set two variables proportion----'''
        # =============================================================================
        '''---set two variables original---'''
        data_derivative_variables = data_derivative_variables.join(data_merge_2[set_two_variables])
        
        '''---set two variables Z values variables---'''
        for column in set_two_variables:    
            column_name = column + '_z_value'    
            data_derivative_variables[column_name] = (data_merge_2[column] - data_merge_2[column].rolling(window = 5).median()) / data_merge_2[column].rolling(window = 5).std()
        
        # =============================================================================
        # '''----set three variables proportion----'''
        # =============================================================================
        data_derivative_variables['float_share_to_total_ratio'] = data_merge_2['float_share'] / data_merge_2['total_share']
        data_derivative_variables['free_share_to_total_ratio'] = data_merge_2['free_share'] / data_merge_2['total_share']
        data_derivative_variables['circ_mv_to_total_ratio'] = data_merge_2['circ_mv'] / data_merge_2['total_mv']
        
        # =============================================================================
        # '''----set four variables proportion----'''
        # =============================================================================
        
        data_derivative_variables['open_to_pre_close'] = data_merge_2['open'] / data_merge_2['pre_close']
        data_derivative_variables['high_to_pre_close'] = data_merge_2['high'] / data_merge_2['pre_close']
        data_derivative_variables['low_to_pre_close'] = data_merge_2['low'] / data_merge_2['pre_close']
        data_derivative_variables['low_to_high'] = data_merge_2['low'] / data_merge_2['high']
        data_derivative_variables['high_to_low'] = data_merge_2['high'] / data_merge_2['low']
    
        new_variables = ['open_to_pre_close','high_to_pre_close','low_to_pre_close','low_to_high','high_to_low']
        
        for column in set_four_variables:    
            column_name = column + '_z_value'    
            data_derivative_variables[column_name] = (data_merge_2[column] - data_merge_2[column].rolling(window = 5).median()) / data_merge_2[column].rolling(window = 5).std()
        
        for column in new_variables:    
            column_name = column + '_z_value'    
            data_derivative_variables[column_name] = (data_derivative_variables[column] - data_derivative_variables[column].rolling(window = 5).median()) / data_derivative_variables[column].rolling(window = 5).std()
        
        # =============================================================================
        # add sampling
        # =============================================================================
        
        data_derivative_variables['label'] = data_merge_2['label']
            
        
        '''--------------saving-------------'''
        try:
            pd.io.sql.to_sql(data_derivative_variables, table, engine_daily_stock_variabels ,index = None,if_exists = 'replace') ## change
        except ValueError:
            error_ticks.append(table)
            continue

        if not error_ticks:
            msg = 'Stocks variables calculated successed!' + str(core_index)
            logging.info(msg)

        else:
            logging.warning('Some stocks variables claculation failed, check error ticks' + str(core_index))
            logging.warning(str(error_ticks))
         
    return
        
                
# =============================================================================
# Data Input
# =============================================================================

data_base_address = dict()
data_base_address['capital_flow'] = 'stock_daily_capital_flow'
data_base_address['daily_basic'] = 'stocks_daily_basic'
data_base_address['daily_price'] = 'stocks_price_daily_qfq'
data_base_address['variable_address_1'] = 'stocks_variables_1'
inc_pct = 0.1
dec_pct = 0.05
forward_period = 10
filename = 'variable_1.log'
core_index = cpu_count()
status = 'qfq'


# =============================================================================
# multiprocessing       
# =============================================================================
p = Pool(core_index)  
for i in range(core_index): #4个子进程完成5个任务，所以有一个任务是需要等某个进程空闲再处理
    p.apply_async(sampling_merge, args=(status,data_base_address,filename,i,)) #a是进程处理函数long_time_task的返回结果
print ('等待所有子进程结束...')
p.close()
p.join()#等待所有子进程执行完毕。调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
print ('所有子进程结束...')
    
    
                
                
                
                
                
                
                
                
