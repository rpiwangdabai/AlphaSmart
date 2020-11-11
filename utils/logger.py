#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-10 19:20:24
# @Author  : Hao Wang (tjuhaowang@gmail.com)
# @Link    : link
# @Version : 1.0.0
"""This module is used for project logging."""

import logging
import sys
from functools import wraps
# working directory is always project root
sys.path.append('.')
#pylint: disable=wrong-import-position
import config.user_config as ucfg
#pylint: enable=wrong-import-position
def create_logger(logger_name = __name__, log_file = ucfg.log['logFile']):
    """
    create a logging object and point log file
    """
    logger_current = logging.getLogger(logger_name)
    # level is not set. It depends on basicConfig in running time
    if not logger_current.handlers:
        file_handler = logging.FileHandler(log_file)
        log_format = '%(asctime)s - %(name)s - %(message)s'
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        logger_current.addHandler(file_handler)
    return logger_current

def logger_decorator(logger_name = __name__):
    """
    Decorator log call and return from current funtion
    """
    def logger_function(target_function):
        @wraps(target_function)
        def decorated_function(*args, **kwargs):
            logger_current = logging.getLogger(logger_name)
            logger_current.debug("Calling: %s", target_function.__name__)
            logger_current.debug("args: %s", str(args))
            logger_current.debug("kwargs: %s", str(kwargs))
            try:
                result = target_function(*args, **kwargs)
                logger_current.debug("Return from: %s", target_function.__name__)
                logger_current.debug("Returned : {str(result)}")
                return result
            except:
                logging.exception('Got exception: %s', target_function.__name__)
                raise
        return decorated_function
    return logger_function
