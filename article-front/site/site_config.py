# coding: utf-8
# site configs

ENABLE_CROSSDOMAIN = True

ES_HOSTS = ['localhost:32769']
ES_TITLE_SEARCH_URL = 'article/_suggest'
ES_TITLE_SEARCH_BODY = """
{{
  "title-suggest": {{
    "text" : "{search_string}",
    "completion" : {{
        "field" : "suggest"
    }}
  }}
}}
"""

ES_QUERY_MATCH_URL = 'article/composition/_search'
ES_QUERY_MATCH_BODY = """
{{
  "fields": [ "title", "abstract", "number", "_id" ],
  "from": {page_from},
  "size": {page_size},
  "query": {{
    "bool": {{
      "should": [
        {{
          "match": {{
            "title.primitive": "{search_string}"
          }}
        }},
        {{
          "match": {{
            "abstract": "{search_string}"
          }}
        }}
      ]
    }}
  }}
}}
"""

ES_QUERY_DETAIL_URL = 'article/composition/_search'
ES_QUERY_DETAIL_BODY = """
{{
  "query": {{
    "ids" : {{
        "values" : ["{id}"]
    }}
  }}
}}
"""
