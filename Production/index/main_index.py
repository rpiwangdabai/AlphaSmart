#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020

@author: Roy
"""

import sys
sys.path.append('/Users/Roy/Documents/Investment/Production/') 

from data.get_data.TuShare.get_data_and_save import GetDataAndSave

'''-----------set up-----------'''
# set token
token = '260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c'
# set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/index'
# ticks data
ticks = ['399300.SZ']

'''-----------download fund data and save to sql-----------'''
d_a_s = GetDataAndSave(token, data_base_address)
failed_ticks = d_a_s.get_data_and_save_bulk(ticks, types = 'index')








