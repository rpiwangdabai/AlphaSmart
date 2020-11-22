#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-22 09:41:57
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

import sys
# working directory is always project root
sys.path.append('.')
import alphasmart.config.user_config as ucfg
import alphasmart.config.data_config as dcfg
from alphasmart.datalib.data_manager import TushareDatabaseManager

TUSHARE_MANAGER = None
ACTIVE_MANAGER = None

def init():
    global TUSHARE_MANAGER
    TUSHARE_MANAGER = TushareDatabaseManager(token = ucfg.tushare['token'],
        database_dict= ucfg.mysqlServer['tushare']) 
    TUSHARE_MANAGER.set_ticks_filter(arket_types = dcfg.tushare['fund']['market_types'],
        invest_types = dcfg.tushare['fund']['invest_types'],
        fund_types = dcfg.tushare['fund']['fund_types'],
        date_limit = dcfg.tushare['fund']['date_limit'])