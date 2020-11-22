#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-21 21:58:54
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

import os
import pandas as pd
import numpy as np

from alphasmart.datalib.data_manager import TushareDatabaseManager
import alphasmart.config.user_config as ucfg
import alphasmart.config.data_config as dcfg

tushare_manager = TushareDatabaseManager(token = ucfg.tushare['token'],
        database_dict= ucfg.mysqlServer['tushare'], active_database = 'indexes')
data = tushare_manager.get_local_single_tick_dataframe("399300.SZ")
print(data)