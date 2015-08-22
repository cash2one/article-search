# coding: utf-8

import logging
import logging.config
import os
import sys

import common.core as core
import importer.db_importer as db_importer
from importer.db_models import Composition
from storage.dummy_storage import DummyStorage
from storage.es_storage import ESStorage
import app_config

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger() # get root logger

class MofanggeDBParser(db_importer.DefaultDBDataParser):
    def parse(self, obj):
        return  { 
                    'originalID' : obj.original_id, 
                    'title' : obj.title, 
                    'keywords' : obj.keywords, 
                    'abstract' : obj.abstract, 
                    'content' : obj.content, 
                    'grade' : obj.grade, 
                    'style' : obj.style, 
                    'number' : obj.number,
                    'score' : obj.score, 
                    'source' : obj.source,
                    'suggest' : obj.title, # add title as suggest field simply
                }


class MofanggeImporter(db_importer.DBDataImporter):
    parser_class = MofanggeDBParser
    model_class = Composition


if __name__ == '__main__':
    logger.info('import mofangge data from database')
    importer = MofanggeImporter(db_config=app_config.DB_IMPORTER_DATABASES)
    #output_storage = DummyStorage()
    output_storage = ESStorage(app_config.ES_STORAGE_CONFIG['HOSTS'],
                                index=app_config.ES_STORAGE_CONFIG['INDEX'], 
                                doc_type=app_config.ES_STORAGE_CONFIG['DOC_TYPE'], 
                                doc_index=app_config.ES_STORAGE_CONFIG['DOC_MAPPING'])
    worker = core.DataImport(importer_inst=importer, storage_inst=output_storage)
    worker.start()
    worker.join()