#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020
@author: Roy
"""
import sys
import logging
sys.path.append('.')
import alphasmart.config.user_config as ucfg
import alphasmart.config.data_config as dcfg
from alphasmart.datalib.data_manager import TushareDatabaseManager
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    #''-----------set up-----------'''
    manager = TushareDatabaseManager(token = ucfg.tushare['token'],
        database_dict= ucfg.mysqlServer['tushare'], active_database = 'indexes')
    #'''-----------get basics-------------'''
    manager.download_basics('indexes')
    #'''-----------select ticks-------------'''
    # index_ticks = manager.set_ticks(dcfg.tushare['index']['ticks'])
    #'''-----------download fund data and save to sql-----------'''
    failed_ticks = manager.download_multi_ticks_data_save('indexes', 
        dcfg.tushare['index']['ticks'])
