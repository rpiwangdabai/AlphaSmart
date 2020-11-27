#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-21 21:58:54
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
import logging
from alphasmart.config import setting
import alphasmart.config.data_config as dcfg

setting.init()
logging.basicConfig(level = logging.DEBUG)

data = setting.TUSHARE_MANAGER.get_local_single_tick_dataframe("399300.SZ", 
    'trade_date''20100101', '20121231')
print(data)
