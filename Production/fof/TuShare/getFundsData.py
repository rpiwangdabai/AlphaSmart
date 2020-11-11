#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 20:50:03
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0


import sys
# working directory is always project root
sys.path.append('.')
from DataLib.DataLoader import TushareFundsLoader

if __name__ == '__main__':
    # set up
    loader = TushareFundsLoader()
    # get basics
    loader.getBasicsAndSave()
    # select ticks
    fundTicks = loader.selectTicks()
    # download fund data and save to sql
    failedTicks = loader.getTickDataAndSaveBulk()
    print(failedTicks)
    