# coding: utf-8

import logging
import os
import re
import sys
import types
import random
from multiprocessing import Pool
from functools import partial
import Queue
import threading

import common.decorator as decorator
from importer import DataImporter

logger = logging.getLogger(__name__)

class DefaultFileDataParser(object):
    """
        Work to Do :
        - read in file content
        - parse and return an object
    """
    def parse(self, filepath):
        return {'file_path':filepath}

# work around for using class method with multiprocessing.Pool
# refer to : http://www.rueckstiess.net/research/snippets/show/ca1d7d90
class WorkerFunc(object):
    def __init__(self, parser):
        self.parser = parser
    def __call__(self, file_pair):
        record = self.parser.parse(os.path.join(file_pair[0], file_pair[1]))
        return record

# file data importer class
class FileDataImporter(DataImporter, threading.Thread):
    parser_class = DefaultFileDataParser

    def __init__(self, root_path, ext='.html'):
        threading.Thread.__init__(self)
        if not os.path.exists(root_path):
            raise Exception('path({path}) not exist'.format(path=root_path))
        self.root_path = root_path
        self.ext_filter = ext
        self.__data_queue = Queue.Queue()
        self.__data_end_event = threading.Event()

    def data(self):
        while not (self.__data_end_event.isSet() and self.__data_queue.empty()):
            try:
                obj = self.__data_queue.get(block=True, timeout=10)
            except Queue.Empty:
                continue 
            else:
                self.__data_queue.task_done()
                yield obj

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def run(self, processes=4, chunksize=100):
        # generate list of (path, fname)
        def traverse_filter_ext(dir_path, ext):
            for root, dirs, files in os.walk(dir_path):
                for fname in files:
                    if fname and fname.endswith(ext):
                        logger.debug('generate file: {root}/{fname}'.format(root=root, fname=fname))
                        yield (root, fname)
                for dpath in dirs:
                    traverse_filter_ext(dpath, ext)

        # run func start
        try:
            # create pool and run
            pool = Pool(processes=processes)
            func = WorkerFunc(self.parser_class())
            for record in pool.imap(func, traverse_filter_ext(self.root_path, self.ext_filter), chunksize=chunksize):
                if record:
                    self.__data_queue.put(record)
                else:
                    logger.warn('parse error, skip record')
            # send data end event
            self.__data_end_event.set()
            pool.close()
            pool.join()
        except:
            raise

