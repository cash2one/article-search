# coding: utf-8

import logging
import logging.config
import os
import sys

import common.core as core
import importer.db_importer as db_importer
from importer.db_models import BackendComposition
from storage.dummy_storage import DummyStorage
from storage.es_storage import ESStorage
import app_config

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger() # get root logger

class BackendDBParser(db_importer.DefaultDBDataParser):
    def parse(self, obj):
        return  { 
                    'originalID' : obj.id, 
                    'title' : obj.title, 
                    'keywords' : obj.tags, 
                    'abstract' : obj.abstract, 
                    'content' : obj.content, 
                    'grade' : obj.grade, 
                    'style' : obj.atype, 
                    'number' : obj.number,
                    'score' : 100, 
                    'source' : obj.source,
                    'suggest' : obj.title, # add title as suggest field simply
                }


class BackendDBImporter(db_importer.DBDataImporter):
    parser_class = BackendDBParser
    model_class = BackendComposition


if __name__ == '__main__':
    logger.info('import backend data from database')
    importer = BackendDBImporter(db_config=app_config.DB_IMPORTER_DATABASES)
    #output_storage = DummyStorage()
    output_storage = ESStorage(app_config.ES_STORAGE_CONFIG['HOSTS'],
                                index=app_config.ES_STORAGE_CONFIG['INDEX'], 
                                doc_type=app_config.ES_STORAGE_CONFIG['DOC_TYPE'], 
                                doc_index=app_config.ES_STORAGE_CONFIG['DOC_MAPPING'])
    worker = core.DataImport(importer_inst=importer, storage_inst=output_storage)
    worker.start()
    worker.join()