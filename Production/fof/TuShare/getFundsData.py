#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:34:59 2020

@author: Roy
"""
import os
import sys
import tushare as ts 
import pandas as pd
import numpy as np
import logging
import time
from sqlalchemy import create_engine
# working directory is always project root
os.getcwd()
sys.path.append('.')
from Config.userConfig import FUNDS_DB_PATH, FUND_LIST_FILE_2, FUND_LIST_FILE_3, TS_TOKEN
from Utils.GetDataAndSave import GetDataAndSave
    
    
if __name__ == '__main__':
    '''-----------set up-----------'''
    # set token
    token = TS_TOKEN 
    # set data_base_address
    data_base_address = FUNDS_DB_PATH
    # ticks data
    funds_data = pd.read_csv(FUND_LIST_FILE_3)
    fund_tick = list(funds_data['ts_code'])
    '''-----------download fund data and save to sql-----------'''
    dataSave = GetDataAndSave(token, data_base_address)
    failed_ticks = dataSave.get_data_and_save_bulk(fund_tick, types = 'fund')
    print(failed_ticks)
    

    
    
    
    
    