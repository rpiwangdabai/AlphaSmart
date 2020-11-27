#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-27 13:38:14
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

import os
import pandas as pd
import numpy as np
import logging
from alphasmart.config import setting
from alphasmart.portfoliolib.securities import Index

setting.init()
logging.basicConfig(level = logging.DEBUG)


my_security = Index("399300.SZ")
my_security.get_index_tushare_data()
pair_security = Index('000001.SH')
pair_security.get_index_tushare_data()
my_security.calculate_security_correlation(pair_security,
    ["close", "close"], ['20100101', '20200101'])
