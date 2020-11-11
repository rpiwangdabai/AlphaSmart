#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 20:50:03
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0


import sys
# working directory is always project root
sys.path.append('.')
import config.user_config as ucfg
import config.data_config as dcfg
from datalib.data_loader import TushareFundsLoader


if __name__ == '__main__':
    # set up
    loader = TushareFundsLoader(token = ucfg.tushare['token'], database_address = ucfg.mysqlServer['fundDatabase'])
    # get basics
    loader.download_basics_and_save()
    # select ticks
    fundTicks = loader.select_ticks(market_types =dcfg.tushare['fund']['marketTypes'],
        invest_types = dcfg.tushare['fund']['investTypes'],
        fund_types = dcfg.tushare['fund']['fundTypes'],
        date_limit = dcfg.tushare['fund']['dateLimit'])
    # download fund data and save to sql
    failedTicks = loader.download_ticks_data_and_save()
    print(failedTicks)
    