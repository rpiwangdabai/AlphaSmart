#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:34:59 2020

@author: Roy
"""
import tushare as ts 
import pandas as pd
import logging
from sqlalchemy import create_engine
import traceback
import time

class StockDailyCapitalFlow():
    """
    Class for downloading stock daily capital flow data from Tushare.
    IMPORTANT:
        data begin from 20100105
    
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
    
    def __init__(self, token, data_base_address,stock_ticks_data_base_address, filename = 'stock_daily_capital_flow.log'):
        
        self.token = token
        self.data_base_address = data_base_address
        # setup tushare token        
        ts.set_token(token)
        self.ts_pro = ts.pro_api()
        # build up database connection
        self.conn = create_engine(self.data_base_address, encoding ='utf8')
        self.conn_ticks = create_engine(stock_ticks_data_base_address, encoding ='utf8')
        
        logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=filename,
                filemode='a')


    def get_data_and_save_bulk(self):
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
        # get all stocks ticks
        sql_cmd = "SELECT * FROM `liseted stock list`;"
        ticks_data = pd.read_sql(sql=sql_cmd, con=self.conn_ticks)
        ticks = list(ticks_data['ts_code'])
        # # for quick testing only
        # ticks = ticks[:1]
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
                data = self.ts_pro.moneyflow(ts_code=tick)
            except BaseException :
                data = self.ts_pro.moneyflow(ts_code=tick)
             
            if data.empty:
                error_ticks.append(tick)
                continue
            # set lag
            time.sleep(0.3)
            # save data to sql
            try:
                pd.io.sql.to_sql(data, tick[:6], self.conn,index = None,if_exists = 'replace') ## change
            except ValueError:
                error_ticks.append(tick)
                continue
        if not error_ticks:
            logging.info('Stock daily capital flow update successfully!')

        else:
            logging.warning('some data download failed, check error ticks')
            logging.warning(str(error_ticks))
        return error_ticks
    
    def run(self):
        '''
        
        running

        '''
        
        try:
            self.get_data_and_save_bulk()

        except Exception:
            logging.error("错误日志：\n" + traceback.format_exc())


        

if __name__ == '__main__':
    
    '''-----------set up-----------'''
    # set token
    token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'
    # set data_base_address
    data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow'
    stock_ticks_data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
    
    '''-----------download stock data and save to sql-----------'''
    s_d_b = StockDailyCapitalFlow(token, data_base_address,stock_ticks_data_base_address)
    s_d_b.run()
    

    
    
    
    