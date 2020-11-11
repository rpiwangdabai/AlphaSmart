#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-07 22:21:00
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""This module stores user related configure preference."""
import keyring

# mysql DB
mysqlPassword = keyring.get_password("mysql", "root")
mysqlServer =  {
    'password':mysqlPassword,
    'fundDatabase': 'mysql+pymysql://root:'+mysqlPassword+'@localhost:3306/fund',
    'indexesDatabase': 'mysql+pymysql://root:'+mysqlPassword+'@localhost:3306/indexes',
}

# tushare
tushareToken = keyring.get_password("tushare", "root")
tushare  =  {
    'token':tushareToken
}

# logger
log = {
    'logFile':r'./log.txt'
}
