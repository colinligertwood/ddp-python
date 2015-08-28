import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket

import ddp

class DDP_WSHandler(tornado.websocket.WebSocketHandler):
    """
    """
    session_id = None
    def open(self):
        print "New Connection"

    def on_msg_connect(self, msg):
        if msg.version == "1":
            self.sessions = msg.session
            resp = ddp.Connected(msg.session)
            self.write_message(ddp.serialize(resp))
        else:
            msg_obj = ddp.Failed("1")

    def on_msg_ping(self, msg):
        resp = ddp.Pong(msg.id)
        self.write_message(ddp.serialize(resp))

    def on_msg_sub(self, msg):

    def on_message(self, message):
        print "Message Received: {}".format(message)
        msg = ddp.deserialize(message)
        if msg.msg == "connect":
            self.on_msg_connect(msg)
        if msg.msg == "ping":
            self.on_msg_ping(msg)
        if msg.msg == "sub":
            self.on_msg_sub(msg)

    def check_origin(self, origin):
        return True


application = tornado.web.Application([(r'/ws', DDP_WSHandler)])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9980)
    myIP = socket.gethostbyname(socket.gethostname())
    print '*** Websocket Server Started at %s***' % myIP
    tornado.ioloop.IOLoop.instance().start()

