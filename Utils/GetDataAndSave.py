#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-08 20:48:41
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

import os
import sys
import tushare as ts 
import pandas as pd
import numpy as np
import logging
import time
from sqlalchemy import create_engine

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
    
    def __init__(self, token, dataBaseAddress):
        
        self.token = token
        self.dataBaseAddress = dataBaseAddress
        # setup tushare token        
        ts.set_token(token)
        self.ts_pro = ts.pro_api()
        # build up database connection
        self.conn = create_engine(self.dataBaseAddress, 
            encoding ='utf8')
        

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


    def getDataAndSaveBulk(self, ticks, types, calculateLogRet = True, logFile = './log.txt'):
        """
        Downloadind data from Tushare database and save them to the database
        
        Parameters
        --------
            ticks : list
                Funds or stocks ticks
            
            types : str
                asset types. Can be 'fund', 'index', or 'stock'
            
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
        
        logFile
        # setup logger
        log = self.logger(logFile)
        # id count
        i, n = 1, len(ticks)
        # error ticks
        errorTicks = []
        # get fund data and save it to sql
        if types == 'fund':
            while ticks:
                print(i)
                i += 1 
                tick = ticks.pop()
                print(tick, "{:.0%}".format(i/n))
                data = self.ts_pro.fund_nav(ts_code=tick)
                if data.empty:
                    errorTicks.append(tick)
                    continue
                # calculate log return
                if calculateLogRet:
                    data['log_ret'] = np.log(data.adj_nav) - np.log(data.adj_nav.shift(-1))
                # set lag
                time.sleep(0.8)
                # save data to sql
                try:
                    pd.io.sql.to_sql(data, tick.lower(), self.conn, index = None, if_exists = 'replace') ## change
                except ValueError:
                    errorTicks.append(tick)
                    continue
            if not errorTicks:
                log.warning('funds download successed !')
            else:
                log.warning('some data download failed, check error ticks')      
        elif types == 'index':
            while ticks:
                print(i)
                i += 1 
                tick = ticks.pop()
                data = self.ts_pro.index_daily(ts_code=tick)
                if data.empty:
                    errorTicks.append(tick)
                    continue
                # calculate log return
                if calculateLogRet:
                    data['log_ret'] = np.log(data.close) - np.log(data.close.shift(-1))
                # set lag
                time.sleep(0.1)
                # save data to sql
                try:
                    pd.io.sql.to_sql(data, tick.lower(), self.conn,index = None,if_exists = 'replace') ## change
                except ValueError:
                    errorTicks.append(tick)
                    continue
            if not errorTicks:
                log.warning('funds download successed !')
            else:
                log.warning('some data download failed, check error ticks')
        
        return errorTicks

