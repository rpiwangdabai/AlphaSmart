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
import pandas as pd
# import numpy as np
# import Config.userConfig as ucfg
# import Config.dataConfig as dcfg
import logging
from alphasmart.config import setting

class Security():
    """
    Base class for alll securities
    """
    def __init__(self, tick:str, ):
        """
        __init__(self, tick:str):
        """
        self.tick = tick
        self.period = None
        self.period_return = None
        self.vol = None
        self.annualized_return = None
        self.start_date = None
        self.end_date = None
        self._dataframe = pd.DataFrame()
        self.price_filed = None

    def get_security_data(self, start_date:str = None, end_date:str = None):
        """
        get_security_data(self:
        """
        self._dataframe = setting.TUSHARE_MANAGER.get_local_single_tick_dataframe(self.tick,
            start_date, end_date)
        self.start_date, self.end_date = start_date, end_date
        
    def check_date(self, start_date:str = None, end_date:str = None):
        logger = logging.getLogger(__name__)
        if self._dataframe.empty:
            logger.error("Dataframe of tick %s is None", self.tick)
            return False
        return (self.start_date < start_date) and (self.end_date > end_date) and ()

    def calculate_security_correlation(self, pair_security:Security, start_date:str = None, 
        end_date:str = None):
        """
        alculate_security_correlation(self, pair_security)
        """
        logger = logging.getLogger(__name__)
        if not self.check_date(start_date, end_date) and pair_security.check_date(start_date, 
            end_date):
            logger.error("start date: %s and end date %s must be within both security range!\n \
                base: start_date: %s, end date:%s, pari: start_date: %s, end date:%s", start_date,
                end_date, self.start_date, self.end_date, pair_security.start_date, pair_security.end_date)
            raise ValueError("start date and end date must be within both security range!")
        


    def calculate_security_std(self):
        """
        calculateSecurityStd(self):
        """
