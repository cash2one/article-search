# coding: utf-8

import logging
import logging.config
import os
import sys

import django
from django.db import models
from django.conf import settings

import common.core as core
import importer.db_importer as db_importer
from storage.dummy_storage import DummyStorage
from storage.es_storage import ESStorage
import app_config

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger() # get root logger

# define mofangge composition model
class Composition(models.Model):
    """
        +------------+---------------------+------+-----+---------+----------------+
        | Field      | Type                | Null | Key | Default | Extra          |
        +------------+---------------------+------+-----+---------+----------------+
        | DOCID      | bigint(20)          | NO   | PRI | NULL    | auto_increment |
        | ID         | varchar(64)         | NO   | MUL | NULL    |                |
        | OriginalID | varchar(64)         | YES  |     | NULL    |                |
        | Title      | varchar(128)        | YES  |     | NULL    |                |
        | Num        | int(11)             | YES  |     | 0       |                |
        | KeyList    | varchar(256)        | YES  |     |         |                |
        | Abstract   | longtext            | YES  |     | NULL    |                |
        | Url        | varchar(128)        | YES  | UNI | NULL    |                |
        | LabelList  | varchar(256)        | YES  |     |         |                |
        | Style      | tinyint(4)          | YES  |     | NULL    |                |
        | Grade      | tinyint(4)          | YES  |     | NULL    |                |
        | Score      | int(11)             | YES  |     | NULL    |                |
        | Subject    | int(10) unsigned    | YES  |     | NULL    |                |
        | Content    | longtext            | YES  |     | NULL    |                |
        | Site       | tinyint(3) unsigned | YES  |     | NULL    |                |
    """
    doc_id = models.AutoField(primary_key=True)
    md5_id = models.CharField(max_length=64, default=None)
    original_id = models.CharField(max_length=64, null=True, default=None)
    title = models.CharField(max_length=128, null=True, default=None)
    number = models.IntegerField(null=True, default=0)
    keywords = models.CharField(max_length=256, null=True, blank=None)
    abstract = models.TextField(null=True, blank=None)
    url = models.URLField(max_length=128, unique=True, null=True, default=None)
    labels = models.CharField(max_length=256, null=True, blank=None)
    style = models.SmallIntegerField(null=True)
    grade = models.SmallIntegerField(null=True)
    score = models.IntegerField(null=True, default=None)
    subject = models.IntegerField(null=True, default=None)
    content = models.TextField(null=True, blank=None)
    source = models.SmallIntegerField(null=True)

    class Meta:
        db_table = 'mofangge_composition_content'


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
    importer = MofanggeImporter(db_config=app_config.DB_IMPORTER_CONFIG)
    #output_storage = DummyStorage()
    output_storage = ESStorage(app_config.ES_STORAGE_CONFIG['HOSTS'],
                                index=app_config.ES_STORAGE_CONFIG['INDEX'], 
                                doc_type=app_config.ES_STORAGE_CONFIG['DOC_TYPE'], 
                                doc_index=app_config.ES_STORAGE_CONFIG['DOC_MAPPING'])
    worker = core.DataImport(importer_inst=importer, storage_inst=output_storage)
    worker.start()
    worker.join()