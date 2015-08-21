# coding: utf-8

import hashlib
import logging
import threading
import Queue

import common.decorator as decorator


logger = logging.getLogger(__name__)

class StorageThread(threading.Thread):
    def __init__(self, storage, queue, stop_event):
        super(StorageThread, self).__init__()
        self.storage = storage
        self.queue = queue
        self.stop_event = stop_event

    def key(self, value, generator=hashlib.md5()):
        generator.update(str(value))
        return generator.hexdigest()

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def run(self):
        while not (self.stop_event.isSet() and self.queue.empty()):
            try:
                record = self.queue.get(block=False, timeout=1)
            except Queue.Empty:
                # logger.info('storage thread[{thread_id}] queue empty'.format(thread_id=self.name))
                continue
            else:
                self.storage.store(self.key(record), record)
                self.queue.task_done()

# main loop of import process
class DataImport(threading.Thread):
    def __init__(self, importer, storage, storage_pool_size=4):
        threading.Thread.__init__(self)
        self.importer = importer
        self.storage = storage
        self.storage_pool_size = storage_pool_size
    
    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def run(self):
        queue = Queue.Queue()
        # init storage
        stop_event = threading.Event()
        self.storage.init()
        storage_pool = []
        for i in range(self.storage_pool_size):
            t = StorageThread(self.storage, queue, stop_event)
            t.start()
            storage_pool.append(t)
        # start importer
        self.importer.start()
        logger.debug('start import data')
        count = 0
        for record in self.importer.data():
            queue.put(record, block=False)
            count += 1
            if count % 100 == 0:
                logger.info('{num} records processed'.format(num=count))
        logger.info('importer join')
        self.importer.join()
        # wait until queue empty
        logger.info('data queue join')
        queue.join()
        logger.info('send storage stop event')
        stop_event.set() # set stop event to stop all storage threads
        for t in storage_pool:
            t.join()
        logger.info('storage pool joined')
        self.storage.close()
        logger.info('finished data import, {num} records processed'.format(num=count))

