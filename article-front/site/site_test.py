# coding: utf-8
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

def title_suggestion(title_suffix):
    print '==============================='
    print "title:{t}".format(t=title_suffix)
    payload = {'title': title_suffix}
    r = requests.get('http://localhost:8888/title_suggestion', params=payload)
    res = r.json()
    if res['title-suggest']:
        for option in res['title-suggest']:
            print option['text'], option['score']
    else:
        print '无结果'

def query_match(query_string, page=0):
    print '==============================='
    print "query:{s}".format(s=query_string)
    payload = {'search': query_string, 'page': page}
    r = requests.get('http://localhost:8888/query_match', params=payload)
    res = r.json()
    hits = res['hits']
    for hit in hits:
        print '#################################'
        fields = hit['fields']
        print hit['_score'], fields['title'][0], fields['abstract'][0], fields['number'][0]

# test case
# title_suggestion('我')
# title_suggestion('我的')
# title_suggestion('我的妈')
# title_suggestion('我的妈妈')
# title_suggestion('我的妈妈手')

title_suggestion('春')
title_suggestion('春天')
title_suggestion('春天的')
title_suggestion('春天的自')
title_suggestion('春天的自然')

query_match('wo')
query_match('wode')

# query_match('大自然')
# query_match('我的妈妈')
# query_match('我的妈妈', page=1)
