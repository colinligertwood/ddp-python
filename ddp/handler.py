from exceptions import NotImplementedError

import uuid
import tornado.websocket
import ddp

class Handler(tornado.websocket.WebSocketHandler):
    """
    Generic DDP Websockets handler. Subclass this and
    override the msg and event handlers you want to use.
    """
    clients = []
    sessions = {}
    session_id = None

    def write_message(self, message):
        print "sending message:", message
        super(Handler, self).write_message(message)

    # Send Message Events
    def send_connect(self, *args, **kwargs):
        raise NotImplementedError()

    def send_connected(self, session):
        message = ddp.Connected(session)
        self.write_message(ddp.serialize(message))

    def send_failed(self, *args, **kwargs):
        self.write_message(ddp.serialize(ddp.Failed()))

    def send_ping(self, *args, **kwargs):
        raise NotImplementedError()

    def send_pong(self, id):
        message = ddp.Pong(id)
        self.write_message(ddp.serialize(message))

    def send_sub(self, *args, **kwargs):
        raise NotImplementedError()

    def send_unsub(self, *args, **kwargs):
        raise NotImplementedError()

    def send_nosub(self, *args, **kwargs):
        raise NotImplementedError()

    def send_added(self, *args, **kwargs):
        raise NotImplementedError()

    def send_changed(self, *args, **kwargs):
        raise NotImplementedError()

    def send_removed(self, *args, **kwargs):
        raise NotImplementedError()

    def send_added_before(self, *args, **kwargs):
        raise NotImplementedError()

    def send_moved_before(self, *args, **kwargs):
        raise NotImplementedError()

    def send_method(self, *args, **kwargs):
        raise NotImplementedError()

    def send_result(self, *args, **kwargs):
        raise NotImplementedError()

    def send_updated(self, *args, **kwargs):
        raise NotImplementedError()


    # Received Message event Handlers
    def on_connect(self, message):
        if message.session:
            if message.session in self.sessions:
                self.session_id = message.session
                self.session = self.sessions[message.session]
                self.send_connected(self.session_id)
            else:
                self.send_failed()
        else:
            self.session_id = str(uuid.uuid4())
            self.sessions[self.session_id] = {}
            self.session = self.sessions[self.session_id]
            self.send_connected(self.session_id)
    
    def on_connected(self, message):
        raise NotImplementedError()
        
    def on_failed(self, message):
        raise NotImplementedError()
    
    def on_ping(self, message):
        self.send_pong(message.id)
        
    def on_pong(self, message):
        raise NotImplementedError()

    def on_sub(self, message):
        raise NotImplementedError()

    def on_unsub(self, message):
        raise NotImplementedError()

    def on_added(self, message):
        raise NotImplementedError()

    def on_changed(self, message):
        raise NotImplementedError()

    def on_removed(self, message):
        raise NotImplementedError()

    def on_ready(self, message):
        raise NotImplementedError()

    def on_added_before(self, message):
        raise NotImplementedError()

    def on_moved_before(self, message):
        raise NotImplementedError()

    def on_method(self, message):
        raise NotImplementedError()

    def on_result(self, message):
        raise NotImplementedError()

    def on_updated(self, message):
        raise NotImplementedError()

    # Core Websockets Event Handlers
    def on_message(self, message):
        """
        DDP Deserialize the message and pass it on to the
        appropriate received message handler.
        """
        print "received message: ", message
        message = ddp.deserialize(message)
        if message.msg == 'connect':
            self.on_connect(message)
        elif message.msg == 'connected':
            self.on_connected(message)
        elif message.msg == 'failed':
            self.on_failed(message)
        elif message.msg == 'ping':
            self.on_ping(message)
        elif message.msg == 'pong':
            self.on_pong(message)
        elif message.msg == 'sub':
            self.on_sub(message)
        elif message.msg == 'unsub':
            self.on_unsub(message)
        elif message.msg == 'nosub':
            self.on_nosub(message)
        elif message.msg == 'added':
            self.on_added(message)
        elif message.msg == 'changed':
            self.on_changed(message)
        elif message.msg == 'removed':
            self.on_removed(message)
        elif message.msg == 'ready':
            self.on_ready(message)
        elif message.msg == 'addedBefore':
            self.on_added_before(message)
        elif message.msg == 'movedBefore':
            self.on_moved_before(message)
        elif message.msg == 'method':
            self.on_method(message)
        elif message.msg == 'result':
            self.on_result(message)
        elif message.msg == 'updated':
            self.on_updated(message)

    def check_origin(self, origin):
        """
        No security here. Just return true.
        """
        return True
