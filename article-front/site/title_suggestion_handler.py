# coding: utf-8
import random
import tornado.httpclient
import tornado.escape
import tornado.web

from common_handler import CommonHandler
import site_config

class TitleSuggestionHandler(CommonHandler):
    PAGE_SIZE = 10
    ENABLE_CROSSDOMAIN = site_config.ENABLE_CROSSDOMAIN

    @tornado.web.asynchronous
    def get(self):
        # get search argument and filter illegal syntax
        try:
            search_string = self.get_argument("title", None)
            if not search_string:
                raise Exception
            search_string = tornado.escape.url_unescape(search_string)
            print "search title: {s}".format(s=search_string)
        except:
            # return empty list when query string is None
            return self.finish_response(body=[], crossdomain=self.ENABLE_CROSSDOMAIN)
        # construct request
        es_url = "http://{host}/{suffix}".format(
            host=random.choice(site_config.ES_HOSTS), 
            suffix=site_config.ES_TITLE_SEARCH_URL)
        es_body = site_config.ES_TITLE_SEARCH_BODY.format(
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
            raise tornado.web.HTTPError(500)
        json_response = tornado.escape.json_decode(response.body)
        # parse response
        options = json_response['title-suggest'][0]['options']
        print "text: {text}".format(text=json_response['title-suggest'][0]['text'])
        return self.finish_response(body=options, crossdomain=self.ENABLE_CROSSDOMAIN)