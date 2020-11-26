#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 20:50:03
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0


import sys
import logging
# working directory is always project root
sys.path.append('.')
from alphasmart.config import setting

logging.basicConfig(level=logging.DEBUG)
setting.init()

if __name__ == '__main__':
    # set up

    # get basics
    setting.TUSHARE_MANAGER.download_basics('fund')
    # select ticks
    # download fund data and save to sql
    failedTicks = setting.TUSHARE_MANAGER.download_multi_ticks_data_save('fund')
    print(failedTicks)
    