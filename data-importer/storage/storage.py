# coding: utf-8

import logging
import hashlib
import Queue

import common

logger = logging.getLogger(__name__)

# storage base
class Storage(object):
    def __init__(self):
        pass

    def init(self):
        raise NotImplemented

    def store(self, key, value):
        raise NotImplemented

    def close(self):
        raise NotImplemented


class StorageThread(common.utils.CommonThread):
    def __init__(self, storage, queue):
        super(StorageThread, self).__init__()
        self.storage = storage
        self.queue = queue

    def _key(self, value, generator=hashlib.md5()):
        generator.update(str(value))
        return generator.hexdigest()

    def tick(self):
        try:
            record = self.queue.get(block=False, timeout=1)
        except Queue.Empty:
            # logger.info('storage thread[{thread_id}] queue empty'.format(thread_id=self.name))
            return
        else:
            self.storage.store(self._key(record), record)
            self.queue.task_done()




