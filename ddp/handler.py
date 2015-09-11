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


    # Send Message Events
    def on_connect(self, *args, **kwargs):
        raise NotImplementedError()

    def on_connected(self, session):
        message = ddp.Connected(session)

    def on_failed(self, *args, **kwargs):
        message = ddp.Failed()
        self.send_message(message)

    def on_ping(self, *args, **kwargs):
        raise NotImplementedError()

    def on_pong(self, *args, **kwargs):
        raise NotImplementedError()

    def on_sub(self, *args, **kwargs):
        raise NotImplementedError()

    def on_unsub(self, *args, **kwargs):
        raise NotImplementedError()

    def on_nosub(self, *args, **kwargs):
        raise NotImplementedError()

    def on_added(self, *args, **kwargs):
        raise NotImplementedError()

    def on_changed(self, *args, **kwargs):
        raise NotImplementedError()

    def on_removed(self, *args, **kwargs):
        raise NotImplementedError()

    def on_added_before(self, *args, **kwargs):
        raise NotImplementedError()

    def on_moved_before(self, *args, **kwargs):
        raise NotImplementedError()

    def on_method(self, *args, **kwargs):
        raise NotImplementedError()

    def on_result(self, *args, **kwargs):
        raise NotImplementedError()

    def on_updated(self, *args, **kwargs):
        raise NotImplementedError()


    # Received Message event Handlers
    def on_msg_connect(self, message):
        if message.session:
            if message.session in self.sessions:
                self.session_id = message.session
                self.session = self.sessions[message.session]
                self.on_connected(self.session_id)
            else:
                self.on_failed()
        else:
            self.session_id = uuid.uuid4()
        
        self.on_connected(self.session_id)
    
    def on_msg_connected(self, message):
        raise NotImplementedError()
        
    def on_msg_failed(self, message):
        raise NotImplementedError()
    
    def on_msg_ping(self, message):
        raise NotImplementedError()
        
    def on_msg_pong(self, message):
        raise NotImplementedError()

    def on_msg_sub(self, message):
        raise NotImplementedError()

    def on_msg_unsub(self, message):
        raise NotImplementedError()

    def on_msg_added(self, message):
        raise NotImplementedError()

    def on_msg_changed(self, message):
        raise NotImplementedError()

    def on_msg_removed(self, message):
        raise NotImplementedError()

    def on_msg_ready(self, message):
        raise NotImplementedError()

    def on_msg_added_before(self, message):
        raise NotImplementedError()

    def on_msg_moved_before(self, message):
        raise NotImplementedError()

    def on_msg_method(self, message):
        raise NotImplementedError()

    def on_msg_result(self, message):
        raise NotImplementedError()

    def on_msg_updated(self, message):
        raise NotImplementedError()

    # Core Websockets Event Handlers
    def on_message(self, message):
        """
        DDP Deserialize the message and pass it on to the
        appropriate received message handler.
        """
        message = ddp.deserialize(message)
        if message.msg == 'connect':
            self.on_msg_connect(msg)
        elif message.msg == 'connected':
            self.on_msg_connected(msg)
        elif message.msg == 'failed':
            self.on_msg_failed(msg)
        elif message.msg == 'ping':
            self.on_msg_ping(msg)
        elif message.msg == 'pong':
            self.on_msg_pong(msg)
        elif message.msg == 'sub':
            self.on_msg_sub(msg)
        elif message.msg == 'unsub':
            self.on_msg_unsub(msg)
        elif message.msg == 'nosub':
            self.on_msg_nosub(msg)
        elif message.msg == 'added':
            self.on_msg_added(msg)
        elif message.msg == 'changed':
            self.on_msg_changed(msg)
        elif message.msg == 'removed':
            self.on_msg_removed(msg)
        elif message.msg == 'ready':
            self.on_msg_ready(msg)
        elif message.msg == 'addedBefore':
            self.on_msg_added_before(msg)
        elif message.msg == 'movedBefore':
            self.on_msg_moved_before(msg)
        elif message.msg == 'method':
            self.on_msg_method(msg)
        elif message.msg == 'result':
            self.on_msg_result(msg)
        elif message.msg == 'updated':
            self.on_msg_updated(msg)

    def check_origin(self, origin):
        """
        No security here. Just return true.
        """
        return True
