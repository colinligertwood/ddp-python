#import tornado.httpserver
#import tornado.ioloop
#import tornado.web as web
#from sockjs.tornado import transports, SockJSRouter
from twisted.internet import reactor
import cyclone.web as web
from sockjs.cyclone import transports, SockJSRouter

import socket
import signal

class Server(object):
    def __init__(self, handler, baseurl, port):
        self.port = port
        self.baseurl = baseurl
        router = SockJSRouter(handler, self.baseurl)
        # Meteor doesn't obey sockjs url conventions so we patch it on our end to work around
        newurls = []
        for url in router._transport_urls:
            if "websocket" in url[0]:
                newurls.append(url)
            newurls.append((url[0].replace(self.baseurl, self.baseurl + '/sockjs'), url[1], url[2]))
        router._transport_urls = newurls
        self.application = web.Application(router.urls)

    def start(self):
        #self.http_server = tornado.httpserver.HTTPServer(self.application)
        #self.http_server.listen(self.port)
        #self.ioloop = tornado.ioloop.IOLoop.instance()
        #try:
        #    self.ioloop.start()
        #except KeyboardInterrupt:
        #    self.ioloop.stop()
        #    raise

        #HACK Workaround a bug in tornado that prevents server restarts
        #self.ioloop._timeouts = []
        #self.http_server.stop()

        reactor.listenTCP(self.port, self.application)
        reactor.run()        

    def stop(self):
        self.ioloop.stop()

if __name__ == "__main__":
    import handler
    server = Server(handler.Handler, "/", 10000)
    server.start()

