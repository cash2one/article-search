# coding: utf-8
import logging
import os
from multiprocessing import Pool
import Queue
import threading

import django
from django.conf import settings
from django.db import models
from django.forms import model_to_dict

import common.decorator as decorator
from importer import DataParser, DataImporter

logger = logging.getLogger(__name__)

class DefaultDBDataParser(DataParser):
    """
        Work to Do :
        - parse django.model object
        - return an dict object
    """
    def parse(self, obj):
        return model_to_dict(obj)

# database data importer class
class DBDataImporter(DataImporter, threading.Thread):
    parser_class = DefaultDBDataParser
    model_class = None

    class ModelClassError(Exception):
        pass

    def __init__(self, db_config):
        threading.Thread.__init__(self)
        self.__data_queue = Queue.Queue()
        self.__data_end_event = threading.Event()
        # check model class
        if not (self.model_class and issubclass(self.model_class, models.Model)):
            raise DBDataImporter.ModelClassError

    def data(self):
        while not (self.__data_end_event.isSet() and self.__data_queue.empty()):
            try:
                obj = self.__data_queue.get(block=True, timeout=1)
            except Queue.Empty:
                continue 
            else:
                self.__data_queue.task_done()
                yield obj

    @decorator.trace_log(logger=logger,lvl=logging.INFO)
    def run(self, processes=4):
        try:
            parser = self.parser_class()
            # TODO : do DB partition here ?
            for obj in self.model_class.objects.all():
                record = parser.parse(obj)
                if record:
                    self.__data_queue.put(record)
                else:
                    logger.warn('parse error, skip record')
            # send data end event
            self.__data_end_event.set()
        except:
            raise
        


