# coding: utf-8

import logging
import threading
import Queue

import common.decorator as decorator
import common.utils as utils
import storage.storage as Store


logger = logging.getLogger(__name__)

# main loop of import process
class DataImport(threading.Thread):
    def __init__(self, importer_inst, storage_inst, storage_pool_size=4):
        threading.Thread.__init__(self)
        self.importer = importer_inst
        self.storage = storage_inst
        self.data_queue = Queue.Queue()
        self.pool = utils.ThreadPool()
        for i in range(storage_pool_size):
            self.pool.add(Store.StorageThread(self.storage, self.data_queue))
    
    @decorator.trace_log(logger=logger, lvl=logging.INFO)
    def run(self):
        # init storage
        self.storage.init()
        # start storage thread pool
        self.pool.start()
        # start importer
        self.importer.start()
        logger.debug('start import data')
        # put data into queue
        count = 0
        for record in self.importer.data():
            self._put_data(record)
            count += 1
        # importer stop
        self.importer.join()
        # wait until queue empty
        self.data_queue.join()
        logger.info('stop storage thread pool')
        self.pool.stop()
        logger.info('join storage thread pool')
        self.pool.join()
        self.storage.close()
        logger.info('finished data import, {count} records processed'.format(count=count))

    @decorator.count(interval=100, enable=True, logger=logger, lvl=logging.INFO)
    def _put_data(self, record):
        self.data_queue.put(record, block=False)