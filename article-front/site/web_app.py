# coding: utf-8
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from tornado.options import define, options

from title_suggestion_handler import TitleSuggestionHandler
from query_match_handler import QueryMatchHandler
from query_detail_handler import QueryDetailHandler

import site_config

reload(sys)
sys.setdefaultencoding('utf-8')

define("debug",default=True,help="Debug Mode",type=bool)
define("port", default=5000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    HELP_STRING = """
    <h2>Usage :</h2><br/>
        <p>/ - show this help.</p>
        <p>/title_suggestion?title=xxxx - give out title suggestions.</p>
        <p>/query_match?search=xxxx&page=1 - return brief search results.</p>
        <p>/query_detail?article_id=xxxx - return detail search result.</p>
    """

    def get(self):
        self.write(self.HELP_STRING)
        self.set_header("Content-Type", "text/html")


def main():
    print('start tornado web')
    tornado.options.parse_command_line()
    if options.debug:
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/ngapp/(.*)", tornado.web.StaticFileHandler, {"path":"app"}),
            (r"/title_suggestion", TitleSuggestionHandler),
            (r"/query_match", QueryMatchHandler),
            (r"/query_detail", QueryDetailHandler),
        ], **options.as_dict())
    else:
        application = tornado.web.Application([
            (r"/", MainHandler),
            (r"/title_suggestion", TitleSuggestionHandler),
            (r"/query_match", QueryMatchHandler),
            (r"/query_detail", QueryDetailHandler),
        ], **options.as_dict())
   
    tornado.httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient')
    http_server = tornado.httpserver.HTTPServer(application)
    print('listen on port:{port}'.format(port=options.port))
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
