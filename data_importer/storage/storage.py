# coding: utf-8

import logging
import sys
import random

logger = logging.getLogger(__name__)

class NotImplemented(Exception):
    pass

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


# Dummy storage for test
class DummyStorage(Storage):
    def __init__(self, filename='storage.test.'+str(random.randint(0, 65535))):
        super(DummyStorage, self).__init__()
        self.filename = filename
        self.file_handler = None

    def init(self):
        logger.info('init dummy storage')
        self.file_handler = open(self.filename, 'w')

    def store(self, key, value):
        try:
            dump_value = {
                'key' : key,
                'value' : value
            }
            self.file_handler.write(str(dump_value) + '\n')
        except:
            raise

    def close(self):
        self.file_handler.close()


