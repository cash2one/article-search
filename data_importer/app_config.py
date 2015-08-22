# coding: utf-8

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
    'HOSTS' : ['localhost:32000'],
    'INDEX' : 'article',
    'DOC_TYPE' : 'composition',
    'DOC_MAPPING' : ES_COMPOSITION_MAPPING,
}

FILE_IMPORTER_CONFIG = {
    'ROOT_PATH' : '/home/lbjworld/article_project/data/zuowenbao_details',
}

DB_IMPORTER_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'composition',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456',
    }
}