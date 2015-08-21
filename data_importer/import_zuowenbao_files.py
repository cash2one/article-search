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
from storage.storage import DummyStorage
from storage.es_storage import ESStorage 

reload(sys)
sys.setdefaultencoding('utf-8')

logging.config.fileConfig('logging.conf')
logger = logging.getLogger() # get root logger


class ZuowenbaoParser(file_importer.DefaultFileDataParser):
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
                    if tag in ZuowenbaoParser.GRADE_LIST:
                        grade = ZuowenbaoParser.GRADE_DICT.get(tag, 0)
                    elif tag in ZuowenbaoParser.STYLE_LIST:
                        style = ZuowenbaoParser.STYLE_DICT.get(tag, 0)
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
                        'source' : ZuowenbaoParser.source,
                        'suggest' : title, # add title as suggest field simply
                    }
            except:
                logger.exception('parse error, file:{filepath}'.format(filepath=filepath))
                return None


class ZuowenbaoImporter(file_importer.FileDataImporter):
    parser_class = ZuowenbaoParser



DOC_INDEX = {
    "mappings" : {
        "composition" : {
            "properties":
            {
                "abstract":
                {
                    "type":"string",
                    "indexAnalyzer":"mmseg_simple",
                    "searchAnalyzer":"mmseg_simple"
                },
                "content":
                {
                    "type":"string",
                    "indexAnalyzer":"mmseg_simple",
                    "searchAnalyzer":"mmseg_simple"
                },
                "keywords":
                {
                    "type":"string",
                    "index":"not_analyzed"
                },
                "originalID":
                {
                    "type":"string",
                    "index":"not_analyzed"
                },
                "source":
                {
                    "type":"string",
                    "index":"not_analyzed"
                },
                "title": {
                    "type": "multi_field",
                    "fields": {
                        "title": {
                            "type": "string",
                            "store": "no",
                            "term_vector": "with_positions_offsets",
                            "analyzer": "pinyin_ngram_analyzer",
                            "boost": 10
                        },
                        "primitive": {
                            "type": "string",
                            "store": "yes",
                            "analyzer": "mmseg_simple"
                        }
                    }
                },
                "number":
                {
                    "type":"long"
                },
                "grade":
                {
                    "type":"long"
                },
                "style":
                {
                    "type":"long"
                },
                "suggest" :
                { 
                    "type" : "completion",
                    "index_analyzer" : "mmseg_simple",
                    "search_analyzer" : "mmseg_simple",
                    "payloads" : True
                }
            }
        }
    }
}


if __name__ == '__main__':
    ROOT_DIR = '/home/lbjworld/article_project/data/zuowenbao_details'

    logger.info('import zuowenbao data from files')
    importer = ZuowenbaoImporter(root_path=ROOT_DIR)
    #output_storage = DummyStorage()
    output_storage = ESStorage(['localhost:32769'],
                                        index='article', doc_type='composition', 
                                        doc_index=DOC_INDEX)
    worker = core.DataImport(importer=importer, storage=output_storage)
    worker.start()
    worker.join()
