#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-09 20:22:02
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""
Portfolio module to consist a portfolio
"""
# import os
# import pandas as pd
# import numpy as np
from alphasmart.portfoliolib.securities import (
    Security,
    Cash,
    Index
    )

class Portfolio():
    """
    Portfolio base class
    """
    def __init__(self):
        self.security_holding = dict()
        self.statistics = dict()
        self.strategy = None

    def add_security(self, security:Security, amount:float):
        """
        add_security(self, security:Security, amount:float)
        """
        self.security_holding[security.tick] = amount

    def rebalance(self):
        """
        rebalance(self)
        """
