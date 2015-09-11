import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket

class Server(object):
    def __init__(self, route, handler, port=9999):
        self.route = route
        self.handler = handler
        self.application = tornado.web.Application([(route, handler)])

    def start():
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.listen(self.port)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop.start()
