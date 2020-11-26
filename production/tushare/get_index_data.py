#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020
@author: Roy
"""
import sys
import logging
sys.path.append('.')
import alphasmart.config.data_config as dcfg
from alphasmart.config import setting

logging.basicConfig(level=logging.DEBUG)
setting.init()

if __name__ == '__main__':

    #'''-----------get basics-------------'''
    setting.TUSHARE_MANAGER.download_basics('indexes')
    #'''-----------select ticks-------------'''
    # index_ticks = manager.set_ticks(dcfg.tushare['index']['ticks'])
    #'''-----------download fund data and save to sql-----------'''
    failed_ticks = setting.TUSHARE_MANAGER.download_multi_ticks_data_save('indexes',
        dcfg.tushare['index']['ticks'])
