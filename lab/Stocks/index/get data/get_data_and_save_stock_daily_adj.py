#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:34:59 2020

@author: Roy
"""
import tushare as ts 
import pandas as pd
import numpy as np
import logging
from sqlalchemy import create_engine
import time

class GetDataAndSave():
    """
    Class for downloading data from Tushare.
    
    Parameters
    --------
        token : str
            Tushare token

        data_base_address : str
            Database address for data storage

        
    Attributes
    --------
    
    error_ticks : list
        ticks that don't get any data from the Thushare servers.
        

    Notes
    --------
    """
    
    def __init__(self, token, data_base_address):
        
        self.token = token
        self.data_base_address = data_base_address
        # setup tushare token        
        ts.set_token(token)
        self.ts = ts
        # build up database connection
        self.conn = create_engine(self.data_base_address, encoding ='utf8')
        

    def logger(self,log_file = './log.txt'):
        """
        Set up logger
        
        Parameters
        --------
            log_file : str
                logger address
                
        Attributes
        --------
            None
    
        Notes
        --------
        """
        
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)   # Log等级总开关
         
        # 第二步，创建一个handler，用于写入日志文件

        fh = logging.FileHandler(log_file, mode='a')
        fh.setLevel(logging.DEBUG)  # 用于写到file的等级开关
         
        # 第三步，再创建一个handler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)    # 输出到console的log等级的开关
         
        # 第四步，定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger



    def get_data_and_save_bulk(self,ticks,calculate_log_ret = True, log_file = './log.txt'):
        """
        Downloadind data from Tushare database and save them to the database
        
        Parameters
        --------
            ticks : list
                Funds or stock ticks
            
            calculate_log_ret: bool. Default is True
                Calcauate assets log return and save them in the database

            log_file : str
                logger address
                
        Attributes
        --------
            error_ticks: list
                Ticks that can't get responded from the Tushare server. 
    
        Notes
        --------
        """
        
        log_file
        # setup logger
        log = self.logger(log_file)
        # id count
        i = 1
        # error ticks
        error_ticks = []
        # get fund data and save it to sql
        while ticks:
            print(i)
            i += 1 
            tick = ticks.pop()
            try:
                data = self.ts.pro_bar(ts_code=tick, adj='hfq')
            except BaseException :
                data = self.ts.pro_bar(ts_code=tick, adj='hfq')
            if data.empty:
                error_ticks.append(tick)
                continue
            # set lag
            # time.sleep(0.3)
            # save data to sql
            try:
                pd.io.sql.to_sql(data, tick + '_hfq', self.conn,index = None,if_exists = 'replace') ## change
            except ValueError:
                error_ticks.append(tick)
                continue
        if not error_ticks:
            log.warning('funds download successed !')
        else:
            log.warning('some data download failed, check error ticks')
        return error_ticks

if __name__ == '__main__':
    
    '''-----------set up-----------'''
    # set token
    token = '260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c'
    # set data_base_address
    data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_hfq'
    # ticks data
    stocks_data = pd.read_csv('/Users/Roy/Documents/Investment/Investment_lab/Stocks/index/stock_ticks.csv')
    stocks_tick = list(stocks_data['ts_code'])
    
    '''-----------download stock data and save to sql-----------'''
    d_a_s = GetDataAndSave(token, data_base_address)
    failed_ticks = d_a_s.get_data_and_save_bulk(stocks_tick)
    

    
    
    
    
    