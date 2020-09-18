# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 18:05:01 2020

@author: Lenovo
"""

from variables_merge import VariableMerge

'''-----------set up-----------'''    # set data_base_address
data_base_address = 'mysql+pymysql://root:ai3ilove@localhost:3306/stock_daily_capital_flow'

'''-----------merge stocks variables-----------'''
vm = VariableMerge(data_base_address,data_base_name = 'Stock_daily_capital_flow')
vm.run()
    