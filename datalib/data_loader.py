#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-08 20:48:41
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
''' Modules both local database downloading, updating and usage '''

import logging
import time
from typing import List
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine
# local
from utils.logger import logger_decorator

class BasicDataLoader():
    '''
    Basic Class for data download
    '''
    def __init__(self, database_address:str):
        self.database_address = database_address
        # build up database connection
        self.conn = create_engine(self.database_address, encoding ='utf8')

#============================TuShare=========================
class TushareDataLoader(BasicDataLoader):
    '''
    Tushare DataBase fund data downloader
    '''
    def __init__(self, token:str, database_address:str):
        BasicDataLoader.__init__(self, database_address)
        # setup tushare
        self.token = token
        ts.set_token(token)
        self.ts_pro_api = ts.pro_api()

        self.ticks = []
        self.error_ticks = []

    @logger_decorator
    def download_basics_and_save(self):
        """
        download_basics_and_save(self)
        """


    def select_ticks(self):
        """
        select_ticks(self)
        """

    def download_single_tick_data(self, tick:str):
        """
        download_single_tick_data(self, tick = None):
        """
        print(tick)
        return pd.DataFrame()

    def download_ticks_data_and_save(self):
        """
        Downloadind data from Tushare database and save them to the database.
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
        logger = logging.getLogger(__name__)
        # id count
        i,  num_ticks = 0, len(self.ticks)
        #print(self.ticks)
        # print(f'total {n} ticks')
        logger.info('total %d ticks', num_ticks)
        # reset error ticks
        self.error_ticks = []
        # get fund data and save it to sql
        while self.ticks:
            print(i)
            i += 1
            tick = self.ticks.pop()
            print(tick, "{:.0%}".format(i/num_ticks))
            data = self.download_single_tick_data(tick)
            if data.empty:
                self.error_ticks.append(tick)
                logger.warning('%s data download failed!', tick)
                continue
            # calculate log return
            #if calculateLogRet:
            #    data['log_ret'] = np.log(data.adj_nav) - np.log(data.adj_nav.shift(-1))
            # set lag
            time.sleep(0.8)
            # save data to sql
            try:
                pd.io.sql.to_sql(data, tick.lower(), self.conn, index = None,
                    if_exists = 'replace') ## change
            except ValueError:
                self.error_ticks.append(tick)
                logger.warning('%s data failed to save to local DB!', tick)
                continue
        if not self.error_ticks:
            logger.info('%s data download successed !', tick)
        else:
            logger.warning('some data download failed, check error ticks')
        return self.error_ticks

    def update_tick_data_and_save(self):
        """
        update_tick_data_and_save(self)
        """


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
    def __init__(self, token:str, database_address:str):
        TushareDataLoader.__init__(self, token, database_address)

        self.market_types = []
        self.invest_types = []
        self.fund_types = []
        self.date_limit = '99999999'

    def download_basics_and_save(self):
        """
        download_basics_and_save(self)
        """
        logger = logging.getLogger(__name__)
        basics = self.ts_pro_api.fund_basic()
        try:
            pd.io.sql.to_sql(basics, 'fundbasic', self.conn, index = None,
                if_exists = 'replace') ## change
        except ValueError:
            logger.warning('fund basic data failed to save to local DB!')


    def set_select_criteria(self, market_types:List[str], invest_types:List[str],
        fund_types:List[str], date_limit:str):
        """set criteria to filter funds"""


    def select_ticks(self):
        """
        select_ticks(self):
        """
        # # get data
        # fund list
        data_list = []

        for market in self.market_types:
            data_list.append(self.ts_pro_api.fund_basic(market = market))
        fund_data = pd.concat(data_list, axis = 0)
        # filter by investment type
        fund_data_choosen = fund_data.loc[fund_data['fund_type'].isin(self.invest_types)]
        # choice fund type
        fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['type'].isin(self.fund_types)]
        fund_data_choosen = fund_data_choosen.loc[fund_data_choosen['found_date'] < self.date_limit]
        self.ticks = list(fund_data_choosen['ts_code'])
        print(str(len(self.ticks)) + "funds are selected!")

        return self.ticks

    def download_single_tick_data(self, tick:str):
        """
        download_single_tick_data(self, tick:str):
        """
        try:
            data = self.ts_pro_api.fund_nav(ts_code = tick)
        except TimeoutError:
            data = pd.DataFrame()
        return data



class TushareIndexLoader(TushareDataLoader):
    """
    TuShare Database Index Data Loader
    """
    def __init__(self, token:str, database_address:str):
        TushareDataLoader.__init__(self, token, database_address)
        self.ticks = []

    def set_ticks(self, ticks:List[str]):
        """
        set_ticks(self, ticks:List[str]):
        """
        self.ticks = ticks
        return self.ticks

    def select_ticks(self):
        """
        select_ticks(self):
        """
        return []

    def download_single_tick_data(self, tick:str):
        """
        download_single_tick_data(self, tick:str):
        """
        try:
            data = self.ts_pro_api.index_daily(ts_code = tick)
        except TimeoutError:
            data = pd.DataFrame()
        return data

    def download_basics_and_save(self):
        """
        download_basics_and_save(self):
        """
        logger = logging.getLogger(__name__)
        basics = self.ts_pro_api.index_basic()
        try:
            pd.io.sql.to_sql(basics, 'indexbasic', self.conn, index = None,
                if_exists = 'replace') ## change
        except ValueError:
            logger.warning('index basic data failed to save to local DB!')

class TushareStockLoader(TushareDataLoader):
    """
    TuShare DB stock data loader
    """


#========================local DataLoader========================#

class LocalDataLoader(BasicDataLoader):
    """
    Base class for other local data loader
    """
    def __init__(self, databaseAddress:str):
        BasicDataLoader.__init__(self, databaseAddress)

    def get_local_data(self, ticks:str):
        """
        get_local_data(self, ticks:str):
        """

class FundDataLoader(BasicDataLoader):
    """
    Load fund data from loacal DB
    """
    def __init__(self, database_address:str):
        BasicDataLoader.__init__(self, database_address)

    # def get_single_tick_dataframe(self, tick:str, start_date:str = None, end_date:str = None):
    #     """
    #     get_single_tick_dataframe(self, tick:str, start_date:str = None, end_date:str = None):
    #     """
