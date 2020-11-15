#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-12 15:40:12
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0



tushare  = {
    # FundofFunds
    # select criteria
    'fund':{
        'marketTypes': ['o', 'e'],
        'investTypes':['股票型','混合型','债券型','混合型', '另类投资型', '货币市场型'],
        'fundTypes' : ['契约型开放式', '契约型封闭式'],
        'dateLimit':'99999999'
    },
    # index
    'index': {
        'ticks':['399300.SZ', '000001.SH', '399006.SZ', '399005.SZ']
    }
}