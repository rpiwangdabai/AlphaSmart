#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 21:03:01
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
module includes all securites
"""
from __future__ import annotations
# import os
import pandas as pd
import logging
from typing import List
from alphasmart.config import setting
from alphasmart.utils.logger import logger_decorator


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
        #self.period_return = None
        #self.vol = None
        #self.annualized_return = None
        self.statistics = dict()
        self.start_date = None
        self.end_date = None
        self._dataframe = pd.DataFrame()
        self.date_field = None

    @logger_decorator(__name__)
    def get_security_tushare_data(self, date_field:str, start_date:str = None, 
        end_date:str = None):
        """
        get_security_data(self:
        """
        self._dataframe = setting.TUSHARE_MANAGER.get_local_single_tick_dataframe(self.tick,
            date_field, start_date, end_date)
        self.start_date = min(self._dataframe[self.date_field])
        self.end_date = max(self._dataframe[self.date_field])

    def check_date(self, start_date:str = None, end_date:str = None):
        logger = logging.getLogger(__name__)
        if self._dataframe.empty:
            logger.error("Dataframe of tick %s is None", self.tick)
            return False
        return (self.start_date < start_date) and (self.end_date > end_date)

    @logger_decorator(__name__)
    def get_series(self, price_field:str, start_date:str = '00000000', 
        end_date:str = '99999999')->pd.Series:
        """
        get_series(self, start_date:str, end_date:str):
        """
        condition_start = self._dataframe[self.date_field] > start_date
        condition_end = self._dataframe[self.date_field] < end_date
        data = self._dataframe[condition_start & condition_end]
        data.index = data[self.date_field]
        return data[price_field].astype(float)

    def calculate_security_correlation(self, pair_security:Security, price_fields:List(str),
        date_range:List(str),  method ='pearson'):
        """
        alculate_security_correlation(self, pair_security)
        """
        logger = logging.getLogger(__name__)
        [start_date, end_date] = date_range
        [base_price_field, pair_price_field] = price_fields
        if not (self.check_date(start_date, end_date) and pair_security.check_date(start_date, 
            end_date)):
            logger.error("start date: %s and end date %s must be within both security range!\n \
                base: start_date: %s, end date:%s, pari: start_date: %s, end date:%s", start_date,
                end_date, self.start_date, self.end_date, pair_security.start_date, pair_security.end_date)
            raise ValueError("start date and end date must be within both security range!")
        return self.get_series(base_price_field, start_date, end_date).corr(pair_security.get_series(
            pair_price_field, start_date, end_date), method = method)


    def calculate_security_std(self):
        """
        calculateSecurityStd(self):
        """

class Index(Security):
    """
    Index class. Derived from seucrities"
    """
    def __init__(self, tick:str):
        Security.__init__(self, tick = tick)
        self.date_field = "trade_date"
    def get_index_tushare_data(self,  start_date:str = None, end_date:str = None):
        """
        get_security_tushare_data(self, start_date:str = None, end_date:str = None)
        """
        return Security.get_security_tushare_data(self, self.date_field, start_date,
            end_date)