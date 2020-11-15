#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-08 21:30:37
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
This module stores configuration to data
"""
# TuShare
tushare  = {
    # FundofFunds
    # select criteria
    'fund':{
        'market_types': ['o', 'e'],
        'invest_types':['股票型','混合型','债券型','混合型', '另类投资型', '货币市场型'],
        'fund_types' : ['契约型开放式'],
        'date_limit':'20140331'
    },
    # index
    'index': {
        'ticks':['399300.SZ', '000001.SH', '399006.SZ', '399005.SZ']
    }
}