# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 11:31:43 2020

@author: Lenovo
"""

import pandas as pd
import logging
import traceback
import numpy as np
from sqlalchemy import create_engine
from multiprocessing import cpu_count
from multiprocessing import Pool
import time
import os
import math


def variable_data_merge(data_base_address,core_index):
    """
    Downloadind data from Tushare database and save them to the database
    
    Parameters
    --------
        adj : str
        None, qfq or hfq.
            
    Returns
    --------
        error_ticks: list
            Ticks that can't get responded from the Tushare server. 

    Notes
    --------
    """

    # get all tables name        
    conn = create_engine(data_base_address, encoding ='utf8')
    cur = conn.execute('''SHOW TABLES''')
    tables_name = cur.fetchall()
    tables_name = tables_name[:100]
    
    # get table column names 
    sql_cmd = "SELECT * FROM `" + tables_name[0][0] + '`;'
    daily_price = pd.read_sql(sql = sql_cmd, con = conn)
    temp_data = pd.read_sql(sql = sql_cmd, con = conn)
    columns = temp_data.columns[2:]

    # build column dataframe
    for column in columns:
        script = column + '=pd.DataFrame()' 
        exec(script)
    
    # core number
    core_number = cpu_count()
    start = int((core_index - 1) * math.ceil(len(tables_name) / core_number))
    end = int(core_index * math.ceil(len(tables_name) / core_number))
    
    # merge all data with the same column
    i = 0
    for name in tables_name[start:end]:
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

    # saving 
    result = []
    error_columns = []
    for column in columns:
        try:
            df_add_to_result = "result.append(" + column + ")" 
            exec(df_add_to_result)
        except ValueError:
            error_columns.append(column)
    
    return (result,error_columns,columns)
    






if __name__ == '__main__':
    
    filename = 'stock_daily_capital_flow.log'
    data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow'
    core_index = cpu_count()
    
    logging.basicConfig(level=logging.INFO,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=filename,
            filemode='a')
    
    # =============================================================================
    # multiprocessing       
    # =============================================================================
    p = Pool(core_index)  
    results = []
    for i in range(1, core_index + 1): #4个子进程完成5个任务，所以有一个任务是需要等某个进程空闲再处理
        results.append(p.apply_async(variable_data_merge, args=(data_base_address,i,))) #a是进程处理函数long_time_task的返回结果
    print ('等待所有子进程结束...')
    p.close()
    p.join()#等待所有子进程执行完毕。调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
    print ('所有子进程结束...')
    
    
    columns = results[0].get()[2]
    for column in columns:
        script = column + '=pd.DataFrame()' 
        exec(script)
    
    er_list = []
    
    for i in results:
        df_list = i.get()[0]
        error_list = i.get()[1]
        columns = i.get()[2]
        for i,column in enumerate(columns):
            merge_script = """
if len( """+ column + """) == 0:
        """+ column + """ = df_list[i].copy()
else:
        """+ column + """ = pd.merge("""+ column + """,df_list[i],on = 'trade_date', how = 'outer')
"""
            exec(merge_script)
        if error_list:
            er_list += error_list

        

    #     if not error_columns:
    #         log_info = self.data_base_name + ' variable merge ssuccessfully!'
    #         logging.info(log_info)

    #     else:
    #         logging.warning('Some volumns merged failed, check error ticks----' + self.data_base_name)
    #         logging.warning(str(error_columns))
    #     return error_columns
        
    # def run(self):
    #     '''
        
    #     running

    #     '''
        
    #     try:
    #         self.variable_data_merge()

    #     except Exception:
    #         logging.error("错误日志：\n" + traceback.format_exc())