# coding: utf-8
import random
import tornado.httpclient
import tornado.escape
import tornado.web

from common_handler import CommonHandler
import site_config


class QueryMatchHandler(CommonHandler):
    PAGE_SIZE = 10
    ENABLE_CROSSDOMAIN = site_config.ENABLE_CROSSDOMAIN

    def check_page_limit(self, page):
        return page >= 0 and page <= 50

    @tornado.web.asynchronous
    def get(self):
        # get search argument and filter illegal syntax
        try:
            search_string = self.get_argument("search", None)
            if not search_string:
                raise Exception
            page_from = int(tornado.escape.url_unescape(self.get_argument("page", "0")))
            if not self.check_page_limit(page_from):
                raise Exception
            page_from = page_from * self.PAGE_SIZE
            search_string = tornado.escape.url_unescape(search_string)
        except:
            return self.finish_response(body=[], crossdomain=self.ENABLE_CROSSDOMAIN)
        # construct request
        es_url = "http://{host}/{suffix}".format(
            host=random.choice(site_config.ES_HOSTS), 
            suffix=site_config.ES_QUERY_MATCH_URL)
        print "page from:{f}".format(f=page_from)
        es_body = site_config.ES_QUERY_MATCH_BODY.format(
            page_from=page_from,
            page_size=self.PAGE_SIZE,
            search_string=search_string)
        es_request = tornado.httpclient.HTTPRequest(
            url=es_url, method='POST', 
            headers={"Content-Type": "application/json"},
            body=tornado.escape.utf8(es_body))
        # send request
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(es_request, callback=self.on_response)

    def on_response(self, response):
        if response.error:
            print response.body
            raise tornado.web.HTTPError(500)
        json_response = tornado.escape.json_decode(response.body)
        # parse response
        print "total hits: {total}".format(total=json_response['hits']['total'])
        # res = {
        #     'total' : json_response['hits']['total'],
        #     'hits' : json_response['hits']['hits']
        # }
        res = json_response['hits']['hits']
        return self.finish_response(body=res, crossdomain=self.ENABLE_CROSSDOMAIN)