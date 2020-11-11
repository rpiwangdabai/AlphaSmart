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
from datalib.data_loader import TushareIndexLoader


if __name__ == '__main__':
    #''-----------set up-----------'''
    loader = TushareIndexLoader(token = ucfg.tushare['token'], 
        database_address = ucfg.mysqlServer['indexesDatabase'])
    #'''-----------get basics-------------'''
    loader.getBasicsAndSave()
    #'''-----------select ticks-------------'''
    index_ticks = loader.set_ticks(dcfg.tushare['index']['ticks'])
    #'''-----------download fund data and save to sql-----------'''
    failed_ticks = loader.download_ticks_data_and_save()
