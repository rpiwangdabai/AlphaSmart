#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 20:31:35 2020

@author: Roy
"""
import pandas as pd

ticker = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/allfundcode.csv')
data = pd.read_csv('/Users/Roy/Documents/Investment/Investment/FoF/data/fund_perf_tonglian.csv')

# delete bond realted fund
data_new = data.copy()

for i in data.index:
    if '债' in data.loc[i]['secShortName']:
        data_new.drop(index = i,inplace = True)











