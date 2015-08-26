# coding: utf-8

import logging
import logging.config
import os
import re
import sys
import json
from bs4 import BeautifulSoup

import common.core as core
import importer.file_importer as file_importer
from storage.dummy_storage import DummyStorage
from storage.es_storage import ESStorage
import app_config

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger() # get root logger


class ZuowenbaoFileParser(file_importer.DefaultFileDataParser):
    source = 'zuowenbao'
    GRADE_DICT = {}
    GRADE_LIST = GRADE_DICT.keys()
    STYLE_DICT = {}
    STYLE_LIST = STYLE_DICT.keys()

    def parse(self, filepath):
        logger.debug('parse file:{filepath}'.format(filepath=filepath))
        with open(filepath) as fp:
            try:
                soup = BeautifulSoup(fp, 'lxml')
                
                keywords = soup.find('meta', attrs={'name':'keywords'})
                if keywords:
                    keywords = keywords.get('content')
                    keywords = keywords.replace(',中考,作文,范文,满分作文,作文宝,春苗作文宝,百度', '')
                else:
                    keywords = ''
                keywords = json.dumps(keywords.split(','), ensure_ascii=False)

                abstract = soup.find('meta', attrs={'name':'description'})
                if abstract:
                    abstract = abstract.get('content')
                    abstract = abstract.split('...')[0] + '...'
                
                title = soup.find('h1', attrs={'class':'title'})
                if title:
                    title = title.text
                else:
                    logger.error('parse title error, file:{filepath}'.format(filepath=filepath))
                    return None
                
                contents = soup.find('div', attrs={'class':'composition-content-wrap'}).contents
                content = ''.join( [ str(s) for s in contents ] )

                originalID = filepath.split('/')[-1].replace('.html', '')

                tags = soup.findAll('li', attrs={'class':'tag'})
                grade, style, number = 0, 0, 0
                for tag in tags:
                    tag = str(tag.text)
                    if tag in ZuowenbaoFileParser.GRADE_LIST:
                        grade = ZuowenbaoFileParser.GRADE_DICT.get(tag, 0)
                    elif tag in ZuowenbaoFileParser.STYLE_LIST:
                        style = ZuowenbaoFileParser.STYLE_DICT.get(tag, 0)
                    elif tag.endswith('字'):
                        number = int(tag.replace('字', ''))
                    else:
                        pass

                return { 
                        'originalID' : originalID, 
                        'title' : title, 
                        'keywords' : keywords, 
                        'abstract' : abstract, 
                        'content' : content, 
                        'grade' : grade, 
                        'style' : style, 
                        'number' : number, 
                        'score' : 0,
                        'source' : ZuowenbaoFileParser.source,
                        'suggest' : title, # add title as suggest field simply
                    }
            except:
                logger.exception('parse error, file:{filepath}'.format(filepath=filepath))
                return None


class ZuowenbaoImporter(file_importer.FileDataImporter):
    parser_class = ZuowenbaoFileParser


if __name__ == '__main__':
    logger.info('import zuowenbao data from files')
    importer = ZuowenbaoImporter(root_path=app_config.FILE_IMPORTER_CONFIG['ROOT_PATH'])
    #output_storage = DummyStorage()
    output_storage = ESStorage(app_config.ES_STORAGE_CONFIG['HOSTS'],
                                index=app_config.ES_STORAGE_CONFIG['INDEX'], 
                                doc_type=app_config.ES_STORAGE_CONFIG['DOC_TYPE'], 
                                doc_index=app_config.ES_STORAGE_CONFIG['DOC_MAPPING'])
    worker = core.DataImport(importer_inst=importer, storage_inst=output_storage)
    worker.start()
    worker.join()
