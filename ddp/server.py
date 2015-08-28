import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

import ddp

class DDP_WSHandler(tornado.websocket.WebSocketHandler):
    """
    """
    def open():
        print "New Connection"

    def on_message(self, message):
        print "Message Received: {}".format(message)
        msg_obj = ddp.deserialize(message)
        print msg_obj

    def check_origin(self, origin):
        return True


application = tornado.web.Application([(r'/ws', DDP_WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9980)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()

