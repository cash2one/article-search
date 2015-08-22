# coding: utf-8

import logging
import random

import storage
import common.decorator as decorator

logger = logging.getLogger(__name__)

# Dummy storage for test
class DummyStorage(storage.Storage):
    def __init__(self, filename='storage.test.'+str(random.randint(0, 65535))):
        super(DummyStorage, self).__init__()
        self.filename = filename
        self.file_handler = None

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def init(self):
        try:
            self.file_handler = open(self.filename, 'w')
        except:
            raise
        else:
            logger.info('init dummy storage')

    def store(self, key, value):
        try:
            dump_value = {
                'key' : key,
                'value' : value
            }
            self.file_handler.write(str(dump_value) + '\n')
        except:
            raise

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def close(self):
        if self.file_handler:
            self.file_handler.close()

    def __delete__(self):
        self.close()