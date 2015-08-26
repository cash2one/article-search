# coding: utf-8

import logging
import threading

import decorator

logger = logging.getLogger(__name__)


class CommonThread(threading.Thread):
    def __init__(self):
        super(CommonThread, self).__init__()
        self.stop_event = threading.Event()

    @decorator.trace_log(logger=logger,lvl=logging.DEBUG)
    def run(self):
        while not self.stop_event.isSet():
            self.tick()

    def stop(self):
        if not self.stop_event.isSet():
            self.stop_event.set()

    def tick(self):
        # this function should be exit in an expected period of time
        pass


class ThreadPool(object):
    class ClassIsNotThread(Exception):
        pass
    class ThreadPoolAlive(Exception):
        pass

    def __init__(self):
        self.__is_alive = False
        self.__pool = []

    def _can_modify_pool(self):
        return (not self.__is_alive)

    def pool_size(self):
        return len(self.__pool)

    def add(self, cls_inst):
        if not self._can_modify_pool():
            raise ThreadPool.ThreadPoolAlive
        if not isinstance(cls_inst, threading.Thread):
            raise ThreadPool.ClassIsNotThread
        self.__pool.append(cls_inst)
        return True

    def start(self):
        try:
            for t in self.__pool:
                t.start()
        except:
            raise
        else:
            self.__is_alive = True

    def stop(self):
        for t in self.__pool:
            t.stop()
        self.__is_alive = False

    def join(self):
        for t in self.__pool:
            t.join()



