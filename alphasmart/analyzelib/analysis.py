#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-28 19:34:10
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
Analysis module.
"""

class Analysis():
    """
    base class to perform analysis before backtesting
    """
    def __init__(self):
        pass

class CorrelationAnalysis(Analysis):
    """
    Correlation analysis
    """
    def __init__(self):
        Analysis.__init__(self)
