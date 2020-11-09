#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020
@author: Roy
"""

import sys
sys.path.append('.')
from Config.userConfig  import INDEXES_DB_PATH, TS_TOKEN
from Config.dataConfig  import INDEX_TICKS
from Utils.GetDataAndSave import GetDataAndSave

'''-----------set up-----------'''
# set data_base_address
# ticks data

'''-----------download fund data and save to sql-----------'''
dataSaver = GetDataAndSave(TS_TOKEN, INDEXES_DB_PATH)
failed_ticks = dataSaver.get_data_and_save_bulk(INDEX_TICKS, types = 'index')








