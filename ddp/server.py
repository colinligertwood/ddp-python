import tornado.httpserver
import tornado.ioloop
import tornado.web
import socket

class Server(object):
    def __init__(self, handler, route="/ddp", port=9999):
        self.handler = handler
        self.route = route
        self.port = port
        self.application = tornado.web.Application([(route, handler)])

    def start(self):
        self.http_server = tornado.httpserver.HTTPServer(self.application)
        self.http_server.listen(self.port)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop.start()

if __name__ == "__main__":
    import handler
    server = Server(handler.Handler)
    server.start()

