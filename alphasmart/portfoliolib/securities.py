#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 21:03:01
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
module includes all securites
"""
# import os
# import pandas as pd
# import numpy as np
# import Config.userConfig as ucfg
# import Config.dataConfig as dcfg
from alphasmart.datalib.data_manager import TushareDatabaseManager

class Security():
    """
    Base class for alll securities
    """
    def __init__(self, tick:str):
        """
        __init__(self, tick:str):
        """
        self.tick = tick
        self.period = None
        self.period_return = None
        self.vol = None
        self.annualized_return = None

    def get_security_data(self, tick:str):
        """
        get_security_data(self, tick):
        """



    def calculate_security_correlation(self, base_security):
        """
        alculateSecurityCorrelation(self, baseSbase_securityecurity)
        """


    def calculate_security_std(self):
        """
        calculateSecurityStd(self):
        """
