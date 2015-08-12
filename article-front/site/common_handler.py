# coding: utf-8
import random
import tornado.httpclient
import tornado.escape
import tornado.web

class CommonHandler(tornado.web.RequestHandler):
    def finish_response(self, body, crossdomain=True):
        self.set_header("Content-Type", "application/json")
        if crossdomain:
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Methods", "GET")
        self.write(tornado.escape.json_encode(body))
        self.finish()
