#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-27 13:38:14
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
Test file for Security Module
"""

import logging
from alphasmart.config import setting
from alphasmart.portfoliolib.securities import (
    Index,
    Fund,
    Cash
    )

setting.init()
logging.basicConfig(level = logging.DEBUG)


my_index = Index("399300.SZ")
my_index.get_index_tushare_data()
pair_index = Index('000001.SH')
pair_index.get_index_tushare_data()
my_index.calculate_security_correlation(pair_index,
    ["close", "close"], ['20100101', '20200101'])

my_fund= Fund('531030of')
my_fund.get_fund_tushare_data()
pair_fund = Fund('530030of')
pair_fund.get_fund_tushare_data()
my_fund.calculate_security_correlation(pair_fund,
    ["adj_nav", "adj_nav"], ['20150101', '20200101'])

my_cash = Cash("CNY")
my_cash.calculate_security_correlation(my_fund,
    ["adj_nav", "adj_nav"], ['20150101', '20200101'])

# cross asset correlation
my_fund.calculate_security_correlation(pair_fund,
    ["adj_nav", "adj_nav"], ['20150101', '20200101'])
