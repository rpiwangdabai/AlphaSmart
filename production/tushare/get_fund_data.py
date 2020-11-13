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
from datalib.data_manager import TushareDatabaseManager


if __name__ == '__main__':
    # set up
    manager = TushareDatabaseManager(token = ucfg.tushare['token'],
        database_dict= ucfg.mysqlServer['tushare'], active_database = 'fund')
    # get basics
    manager.download_basics()
    # select ticks
    manager.set_ticks_filter(arket_types =dcfg.tushare['fund']['market_types'],
        invest_types = dcfg.tushare['fund']['invest_types'],
        fund_types = dcfg.tushare['fund']['fund_types'],
        date_limit = dcfg.tushare['fund']['date_limit'])    
    # download fund data and save to sql
    failedTicks = manager.download_multi_ticks_data_save()
    print(failedTicks)
    