#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020
@author: Roy
"""
import sys
sys.path.append('.')
import config.user_config as ucfg
import config.data_config as dcfg
from datalib.data_manager import TushareDatabaseManager


if __name__ == '__main__':
    #''-----------set up-----------'''
    manager = TushareDatabaseManager(token = ucfg.tushare['token'],
        database_dict= ucfg.mysqlServer['tushare'], active_database = 'indexes')
    #'''-----------get basics-------------'''
    manager.download_basics()
    #'''-----------select ticks-------------'''
    # index_ticks = manager.set_ticks(dcfg.tushare['index']['ticks'])
    #'''-----------download fund data and save to sql-----------'''
    failed_ticks = manager.download_multi_ticks_data_save(dcfg.tushare['index']['ticks'])
