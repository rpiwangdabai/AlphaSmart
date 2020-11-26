#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-21 21:58:54
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0


from alphasmart.config import setting
from alphasmart.portfoliolib.securities import Security
setting.init()

# import alphasmart.config.data_config as dcfg
data = setting.TUSHARE_MANAGER.get_local_single_tick_dataframe("399300.SZ", '20100101',
    '20121231')
print(data)

my_security = Security("399300.SZ")
my_security.get_security_data()
