# coding: utf-8
import random
import tornado.httpclient
import tornado.escape
import tornado.web

from common_handler import CommonHandler
import site_config

class QueryDetailHandler(CommonHandler):
    ENABLE_CROSSDOMAIN = site_config.ENABLE_CROSSDOMAIN

    @tornado.web.asynchronous
    def get(self):
        # get search argument and filter illegal syntax
        try:
            article_id = self.get_argument("article_id", None)
            if not article_id:
                raise Exception
            article_id = str(tornado.escape.url_unescape(article_id))
            print "query article_id: {id}".format(id=article_id)
        except:
            # return empty list when query string is None
            return self.finish_response(body={"error":"article not found"}, 
                                        crossdomain=self.ENABLE_CROSSDOMAIN)
        # construct request
        es_url = "http://{host}/{suffix}".format(
            host=random.choice(site_config.ES_HOSTS), 
            suffix=site_config.ES_QUERY_DETAIL_URL)
        es_body = site_config.ES_QUERY_DETAIL_BODY.format(
            id=article_id)
        es_request = tornado.httpclient.HTTPRequest(
            url=es_url, method='POST',
            headers={"Content-Type": "application/json"},
            body=tornado.escape.utf8(es_body))
        # send request
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(es_request, callback=self.on_response)

    def on_response(self, response):
        if response.error: 
            raise tornado.web.HTTPError(500)
        json_response = tornado.escape.json_decode(response.body)
        # parse response
        print "total hits: {total}".format(total=json_response['hits']['total'])
        res = json_response['hits']['hits']
        if res:
            return self.finish_response(body={"result":res[0]}, 
                                    crossdomain=self.ENABLE_CROSSDOMAIN)
        else:
            return self.finish_response(body={"error":"article not found"}, 
                                        crossdomain=self.ENABLE_CROSSDOMAIN)