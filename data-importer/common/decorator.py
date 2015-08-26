# coding: utf-8

import logging
import inspect
import threading

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


def count(interval=1, enable=True, logger=logging.getLogger(), lvl=logging.DEBUG):
    class CountItem(object):
        def __init__(self):
            self.lock = threading.RLock()
            self.count = 0

        def __repr__(self):
            return 'count:{count}'.format(count=self.count)

        def inc(self):
            with self.lock:
                self.count += 1
                return self.count

    global g_count_map
    g_count_map = {}

    def wrapper(func):
        def wrappered_func(*args, **kwargs):
            res = func(*args, **kwargs)
            if enable:
                func_id = getattr(func, '__name__') + '-' + getattr(func, '__module__')
                ci = g_count_map.get(func_id, CountItem())
                count = ci.inc()
                if count == 1: g_count_map[func_id] = ci
                if count % interval == 0:
                    logger.log(lvl, 'run <{func_id}> count:{count}'.format(func_id=func_id, count=count))
            return res
        return wrappered_func
    return wrapper
