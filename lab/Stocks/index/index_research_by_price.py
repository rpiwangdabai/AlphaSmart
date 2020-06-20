#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:24:23 2020

@author: Roy
"""

import tushare as ts 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import deque
import matplotlib.pyplot as plt


token = '260e5250528465a7bebe4c3f4beaea74d14a3ffcbc8aceab9cd6298c'
ts.set_token(token)

ts_pro = ts.pro_api()

df = ts_pro.daily(ts_code='000001.SZ,600000.SH', start_date='20180701', end_date='20180718')

