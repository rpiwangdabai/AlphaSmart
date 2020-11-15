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
from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker
# local
from alphasmart.utils.logger import logger_decorator
# import config.system_config as scfg



class MysqlDatabaseManager():
    '''
    Basic Class for mysql data manager
    '''
    def __init__(self, database_dict:dict, active_database:str = None):
        logger = logging.getLogger(__name__)
        if not database_dict:
            raise ValueError("database dictionary is empyt!")
        if active_database is not None and (active_database not in database_dict):
            raise ValueError("Active database is not in database dictionary!")

        self._engine_dict = {}
        self._connection_dict = {} 
        self._meta_dict = {}
        for database_name in database_dict:
            database_address = database_dict[database_name]
            
            try:
                # build up database connection engine
                self._engine_dict[database_name] = create_engine(database_address, encoding ='utf8')
                # self._session_dict.update({database_name: sessionmaker(bind = engine)()})
                # connections are kept to keep MetaData not for io
                self._connection_dict[database_name] = self._engine_dict[database_name].connect()
                self._meta_dict[database_name] = MetaData(self._connection_dict[database_name])
            except ConnectionError as conn_error:
                logger.error("Failed to connect to %s !", database_name)
                for conn in self._connection_dict[database_name]:
                    conn.close()
                raise ConnectionError(f"Failed to connect to {database_name}") from conn_error


    @logger_decorator(__name__)
    def write_table(self, dataframe:pd.DataFrame, table_name:str, database_name:str,
        if_exists:str ='fail')->int:
        """
        write data to mysql database
        """
        dataframe.to_sql(table_name, self._engine_dict[database_name].connect(),
            index = None, if_exists = if_exists)
        return 0

    def read_table(self, table_name:str, database_name:str)->pd.DataFrame:
        """
        get table from mysql database
        """
        return pd.read_sql_table(table_name, self._connection_dict[database_name])

    def run_query(self, database_name:str, statement:str):
        """
        run specific mysql query
        """
        logger = logging.getLogger(__name__)
        try:
            with self._engine_dict[database_name].connect() as connection:
                results = connection.excute(statement)  
        except ConnectionError:
            logger.error("Failed to run query at %s !", database_name)

        return results

    def get_select_dataframe(self, database_name:str, statment:str):
        """
        get_select_dataframe(self, database_name:str, statment:str):
        """
        results = self.run_query(database_name, statment)
        data = results.fetchall()
        dataframe = pd.DataFrame()
        if len(data) > 0:
            dataframe = pd.DataFrame(data)
            dataframe.columns = results.keys()
        return dataframe


#============================TuShare=========================
class TushareDatabaseManager(MysqlDatabaseManager):
    '''
    DataBase Manager for Tushare
    '''
    def __init__(self, database_dict:dict, token:str, active_database:str):
        MysqlDatabaseManager.__init__(self, database_dict)
        # setup tushare
        ts.set_token(token)
        self._api = ts.pro_api()
        self._active_database = active_database
        self.target_ticks = []
        self.error_ticks = []
        self.filter = dict()

    @logger_decorator(__name__)
    def download_basics(self, database_name:str):
        """
        download_basics(self, database_name:str = 'fund'). Each database has a basic table.
        """
        logger = logging.getLogger(__name__)
        if database_name == 'fund':
            basics = self._api.fund_basic()
        elif database_name == 'indexes':
            basics = self._api.index_basic()
        elif database_name == 'stock':
            basics = self._api.stock_basic()
        else:
            raise ValueError("Unknown database")
        # write data to mysql
        try:
            self.write_table(basics, database_name + 'basic', database_name, 'replace')
        except ValueError:
            logger.warning('%s Basic data failed to save to local DB!', database_name)

    def set_ticks_filter(self, **kwargs):
        """
        set_ticks_filter(self, **kwargs)
        """
        # for fund
        self.filter['market_types'] = kwargs.get('market_types', ['o', 'e'])
        self.filter['invest_types'] = kwargs.get('invest_types', [])
        self.filter['fund_types'] = kwargs.get('fund_types', [])
        self.filter['date_limit'] = kwargs.get('date_limit', '99999999')

    def generate_target_ticks(self, database_name:str):
        """
        generate_target_ticks(self):
        """
        self.target_ticks = []
        data_list = []
        # if fund
        if database_name == 'fund':
            for market in self.filter['market_types']:
                data_list.append(self._api.fund_basic(market = market))
            fund_data = pd.concat(data_list, axis = 0)
            # filter by investment type
            if self.filter['invest_types']:
                fund_data = fund_data.loc[fund_data['fund_type'].isin(self.filter['invest_types'])]
            # choice fund type
            if self.filter['fund_types']:
                fund_data = fund_data.loc[fund_data['type'].isin(self.filter['fund_types'])]
            fund_data = fund_data.loc[fund_data['found_date'] < self.filter['date_limit']]
            self.target_ticks = list(fund_data['ts_code'])
            print(str(len(self.target_ticks)) + "funds are selected!")

        if database_name == 'index':
            pass

        return self.target_ticks

    def download_single_tick_data(self, tick:str)->pd.DataFrame:
        """
        download_single_tick_data(self, tick = None):
        """
        logger = logging.getLogger(__name__)
        # print(tick)
        data = pd.DataFrame()
        try:
            if self._active_database == 'fund':
                data = self._api.fund_nav(ts_code = tick)
            elif self._active_database == 'indexes':
                data = self._api.index_daily(ts_code = tick)
        except TimeoutError:
            logger.error('TimeoutError in %s ! No data downloaded', tick)
        return data

    def download_multi_ticks_data_save(self, database_name:str, target_ticks:List[str] = None)->int:
        """
        Downloadind data from Tushare database and save them to the database.
        """
        logger = logging.getLogger(__name__)
        if target_ticks:
            self.target_ticks = target_ticks
        elif not self.target_ticks:
            self.target_ticks = self.generate_target_ticks(database_name = database_name)

        # id count
        i,  num_ticks = 0, len(self.target_ticks)
        logger.info('Total %d ticks', num_ticks)
        # reset error ticks
        self.error_ticks = []
        # get fund data and save it to sql
        while self.target_ticks:
            print(i)
            i += 1
            tick = self.target_ticks.pop()
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
                table_name = tick.lower().replace('.',  '')
                print(f'write to table {table_name}')
                self.write_table(data, table_name, database_name,'replace')
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
    # local read
    def get_local_single_tick_dataframe(self, tick:str, start_date:str = None, end_date:str = None):
        """
        get_single_tick_dataframe(self, tick:str, start_date:str = None, end_date:str = None)
        """
