# coding: utf-8
import os

# app config
ES_COMPOSITION_MAPPING = {
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
                "score":
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

ES_STORAGE_CONFIG = {
    'HOSTS' : ['elasticsearch:9200'],
    'INDEX' : 'article',
    'DOC_TYPE' : 'composition',
    'DOC_MAPPING' : ES_COMPOSITION_MAPPING,
}

FILE_IMPORTER_CONFIG = {
    'ROOT_PATH' : os.getenv('IMPORTER_FILE_ROOTPATH'),
}

DB_IMPORTER_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('IMPORTER_DB_NAME'),
        'HOST': os.getenv('IMPORTER_DB_HOST'),
        'PORT': os.getenv('IMPORTER_DB_PORT'),
        'USER': os.getenv('IMPORTER_DB_USER'),
        'PASSWORD': os.getenv('IMPORTER_DB_PASSWORD'),
    }
}
