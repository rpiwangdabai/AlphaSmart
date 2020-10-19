#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:21:10 2020

@author: Roy
"""
import tushare as ts 
import pandas as pd
import logging
from sqlalchemy import create_engine
import traceback
import time


class ListedData():
    """
    Class for downloading listed stock data from Tushare.
    
    Parameters
    --------
        token : str
            Tushare token

        data_base_address : str
            Database address for data storage

    Notes
    --------
    """
    
    def __init__(self, token, data_base_address,log_file_name = 'listed_company_update.log'):

        self.token = token
        self.data_base_address = data_base_address
        # setup tushare token        
        ts.set_token(token)
        self.ts_pro = ts.pro_api()
        # build up database connection
        self.conn = create_engine(self.data_base_address, encoding ='utf8')
        # set up loging
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=log_file_name,
                            filemode='a')

        
        

    def listed_stock_list_update(self):
        """
        Downloadind data from Tushare database and save them to the database
        
        Parameters
        --------
            None
                
        Return
        --------
            None
    
        Notes
        --------
        """

        # download data
        try:
            data = self.ts_pro.stock_basic(exchange='', 
                                            list_status='L', 
                                            fields='ts_code,symbol,name,area,industry,list_date')
            if data.empty:
                logging.warning('Data set is empty, check code!')
            
            pd.io.sql.to_sql(data, 'liseted stock list', self.conn,index = None,if_exists = 'replace') ## change
            # add log
            logging.info('listed stock list download successfully!')
            
        except:
            logging.warning('listed stock list updated ERROR, check code!!')


    def run(self):
        '''
        
        running

        '''
        
        try:
            logging.info('Job starting time at ' + time.strftime("%d/%m/%Y") + ' ' + time.strftime("%I:%M:%S"))
            self.listed_stock_list_update()
        except Exception:
            logging.error("错误日志：\n" + traceback.format_exc())
            
if __name__ == '__main__':
    
    '''-----------set up-----------'''
    # set token
    token = 'ab6bcb87d10984cd4468d5359ce421d30884253c4826c56fd2f4d592'
    # set data_base_address
    data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stocks_daily_basic'
    
    '''-----------download stock data and save to sql-----------'''
    ld = ListedData(token, data_base_address)
    ld.run()  
    

