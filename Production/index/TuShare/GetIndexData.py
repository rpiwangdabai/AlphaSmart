#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 18:16:08 2020
@author: Roy
"""
import sys
from DataLib.DataLoader import TushareIndexLoader

sys.path.append('.')

if __name__ == '__main__':
    #''-----------set up-----------'''
    loader = TushareIndexLoader()
    #'''-----------get basics-------------'''
    loader.getBasicsAndSave()
    #'''-----------select ticks-------------'''
    #indexTicks = loader.selectTicks()
    #'''-----------download fund data and save to sql-----------'''
    failedTicks = loader.getTickDataAndSaveBulk()
