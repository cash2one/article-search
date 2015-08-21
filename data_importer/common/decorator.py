# coding: utf-8

import logging
import inspect

def trace_log(logger=logging.getLogger(), lvl=logging.DEBUG):
    def wrapper(func):
        def wrappered_func(*args, **kwargs):
            func_name = getattr(func, '__name__')
            logger.log(lvl, '[{func_name}] enter'.format(func_name=func_name))
            res = func(*args, **kwargs)
            logger.log(lvl, '[{func_name}] exit'.format(func_name=func_name))
            return res
        return wrappered_func
    return wrapper
