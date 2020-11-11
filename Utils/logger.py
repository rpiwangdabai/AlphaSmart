#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-10 19:20:24
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0

import os
import logging
import sys
from functools import wraps
# working directory is always project root
sys.path.append('.')
import Config.userConfig as ucfg

def createLogger(LoggerName = __name__,logFile = ucfg.log['logFile']):
    """
    create a logging object and point log file
    """
    loggerCurrent = logging.getLogger(LoggerName)
    # level is not set. It depends on basicConfig in running time
    if not loggerCurrent.handlers:
        fileHandler = logging.FileHandler(loggerFile)
        logFormat = '%(asctime)s - %(name)s - %(message)s'
        formatter = logging.Formatter(logFormat)
        fileHandler.setFormatter(formatter)
        loggerCurrent.addHandler(fileHandler)
    return loggerCurrent

def loggerDecorator(loggerName = __name__):
    """
    Decorator log call and return from current funtion
    """
    def loggerFunction(targetFunction):
        @wraps(targetFunction)
        def decoratedFunction(*args, **kwargs):
            loggerCurrent = logging.getLogger(loggerName)
            loggerCurrent.debug(f"Calling: {targetFunction.__name__}")
            oggerCurrent.debug(f"args: {str(args)}")
            oggerCurrent.debug(f"kwargs: {str(kwargs)}")
            try:
                result = targetFunction(*args, **kwargs)
                loggerCurrent.debug(f"Return from: {targetFunction.__name__}")
                loggerCurrent.debug(f"Returned : {str(result)}")
                return result
            except:
                ogging.exception(f'Got exception in {targetFunction.__name__}')
                raise
        return decoratedFunction
    return loggerFunction 
    def 