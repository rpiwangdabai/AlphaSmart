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
from typing import List
import Config.userConfig as ucfg
import Config.dataConfig as dcfg

class BasicDataLoader():
    def __init__(self, databaseAddress:str):
        self.databaseAddress = databaseAddress
        # build up database connection
        self.conn = create_engine(self.databaseAddress, 
            encoding ='utf8')
        self.logger = None 

    def getLogger(self, log_file = './log.txt'):
        """
        Set up logger
        Parameters
        --------
            logFile : str
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
        self.logger = logger
        return logger
        
#============================TuShare=========================
class TushareDataLoader(BasicDataLoader):
    def __init__(self, token:str, databaseAddress:str):
        BasicDataLoader.__init__(self, databaseAddress)
        # setup tushare  
        self.token = token
        ts.set_token(token)
        self.tsProAPI = ts.pro_api()
        
        self.ticks = []
        self.errorTicks = []

    def getBasicsAndSave(self):
        pass

    def selectTicks(self):
        pass
    
    def getSingleTickData(self, tick:str = None):
        return pd.DataFrame()

    def getTickDataAndSaveBulk(self, logFile:str = './log.txt'):
        """
        Downloadind data from Tushare database and save them to the database
        Parameters
        --------
            ticks : list
                Funds or stocks ticks
            types : str
                asset types. Can be 'fund', 'index', or 'stock'

            logFile : str
                logger address
        Attributes
        --------
            errorTicks: list
                Ticks that can't get responded from the Tushare server. 
        Notes
        --------
        """  
        print(logFile)
        # setup logger
        if self.logger is None:
            self.getLogger(logFile)
        # id count
        i,  n = 0, len(self.ticks)
        #print(self.ticks)
        # print(f'total {n} ticks')
        self.logger.info(f'total {n} ticks')
        # reset error ticks
        self.errorTicks = []
        # get fund data and save it to sql
        while self.ticks:
            print(i)
            i += 1 
            tick = self.ticks.pop()
            print(tick, "{:.0%}".format(i/n))
            data = self.getSingleTickData(tick)
            if data.empty:
                self.errorTicks.append(tick)
                self.logger.warning(f'{tick} data download failed!') 
                continue
            # calculate log return
            #if calculateLogRet:
            #    data['log_ret'] = np.log(data.adj_nav) - np.log(data.adj_nav.shift(-1))
            # set lag
            # time.sleep(0.1)
            # save data to sql
            try:
                pd.io.sql.to_sql(data, tick.lower(), self.conn, index = None, if_exists = 'replace') ## change
            except ValueError:
                self.errorTicks.append(tick)
                self.logger.warning(f'{tick} data failed to save to local DB!') 
                continue
        if not self.errorTicks:
            self.logger.info(f'{tick} data download successed !')
        else:
            self.logger.warning('some data download failed, check error ticks') 
        return self.errorTicks

    def updateTickDataAndSave(self, logFile:str = './log.txt'):
        pass


class TushareFundsLoader(TushareDataLoader):
    """
    Class for downloading data from Tushare.
    Parameters
    --------
        token : str
            Tushare token
        databaseAddress : str
            Database address for data storage
    Attributes
    --------
    error_ticks : list
        ticks that don't get any data from the Thushare servers.
    Notes
    --------
    """
    def __init__(self, token:str = ucfg.tushare['token'], 
        databaseAddress:str = ucfg.mysqlServer['fundDatabase']):
        TushareDataLoader.__init__(self, token, databaseAddress)
        if self.logger is None:
            self.getLogger()
    
    def getBasicsAndSave(self):
        basics = self.tsProAPI.fund_basic()
        try:
            pd.io.sql.to_sql(basics, 'fundbasic', self.conn, index = None, if_exists = 'replace') ## change
        except ValueError:
            self.logger.warning(f'fund basic data failed to save to local DB!') 
        
    def selectTicks(self, marketTypes:List[str] = dcfg.tushare['fund']['marketTypes'], 
        investTypes:List[str] = dcfg.tushare['fund']['investTypes'], 
        fundTypes:List[str] = dcfg.tushare['fund']['fundTypes'], 
        dateLimit:str = dcfg.tushare['fund']['dateLimit']) -> None:
        # # get data
        # fund list
        dataList = []
        for m in marketTypes:
            dataList.append(self.tsProAPI.fund_basic(market = m))
        fundData = pd.concat(dataList, axis = 0)
        # filter by investment type
        fundDataChoosen = fundData.loc[fundData['fund_type'].isin(investTypes)]
        # choice fund type 
        fundDataChoosen = fundData.loc[fundData['type'].isin(fundTypes)]
        fundDataChoosen = fundDataChoosen.loc[fundDataChoosen['found_date'] < dateLimit]
        self.ticks = list(fundDataChoosen['ts_code'])
        print(str(len(self.ticks)) + "funds are selected!")

        return self.ticks
    
    def getSingleTickData(self, tick:str):
        try:
            data = self.tsProAPI.fund_nav(ts_code = tick)
        except TimeoutError:
            data = pd.DataFrame()
        return data



class TushareIndexLoader(TushareDataLoader):
    def __init__(self, token:str = ucfg.tushare['token'], 
        databaseAddress:str = ucfg.mysqlServer['fundDatabase']):
        TushareDataLoader.__init__(self, token, databaseAddress)
        self.ticks = dcfg.tushare['index']['ticks']

    def selectTicks(self):
        pass

    def getSingleTickData(self, tick:str):
        try:
            data = self.tsProAPI.index_daily(ts_code = tick)
        except TimeoutError:
            data = pd.DataFrame()
        return data

    def getBasicsAndSave(self):
        basics = self.tsProAPI.index_basic()
        try:
            pd.io.sql.to_sql(basics, 'indexbasic', self.conn, index = None, if_exists = 'replace') ## change
        except ValueError:
            self.logger.warning(f'index basic data failed to save to local DB!') 

class TushareStockLoader(TushareDataLoader):
    pass


#========================local DataLoader========================#

class LocalDataLoader(BasicDataLoader):
    def __init__(self, databaseAddress:str):
        BasicDataLoader.__init__(self, databaseAddress)
    
    def getLocalData(self, ticks:str):
        pass

class FundDataLoader(BasicDataLoader):
    def __init__(self, databaseAddress:str = ucfg.mysqlServer['fundDatabase']):
        BasicDataLoader.__base__(self, databaseAddress)
    
    def getSingleTickDataFrame(self, tick:str, startDate:str = None, endDate:str = None):
        return 

    
