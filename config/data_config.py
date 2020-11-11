#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-08 21:30:37
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

# TuShare
tushare  = {
    # FundofFunds
    # select criteria
    'fund':{
        'marketTypes': ['o', 'e'],
        'investTypes':['股票型','混合型','债券型','混合型', '另类投资型', '货币市场型'],
        'fundTypes' : ['契约型开放式'],
        'dateLimit':'20140331'
    },
    # index
    'index': {
        'ticks':['399300.SZ', '000001.SH', '399006.SZ', '399005.SZ']
    }
}