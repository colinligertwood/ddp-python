from exceptions import NotImplementedError

import uuid
import tornado.websocket
from tornado.ioloop import IOLoop
from sockjs.tornado import SockJSRouter, SockJSConnection

import ddp
from session import Session
from globals import *

class Handler(SockJSConnection):
    """
    Generic DDP Websockets handler. Subclass this and
    override the msg and event handlers you want to use.
    """
    connections = []
    ddp_session = None

    def open(self):
        self.connections.append(self)

    def _send(self, message):
        self.send(message)

    def write_message(self, message):
        IOLoop.instance().add_callback(self._send, ddp.serialize(message))

    # Send Message Events
    def send_connect(self, *args, **kwargs):
        raise NotImplementedError()

    def send_connected(self, session):
        self.write_message(ddp.Connected(session))

    def send_failed(self, *args, **kwargs):
        self.write_message(ddp.Failed())

    def send_ping(self, *args, **kwargs):
        raise NotImplementedError()

    def send_pong(self, id):
        self.write_message(ddp.Pong(id))

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
        global ddp_sessions
        if message.session in ddp_sessions:
            self.ddp_session = ddp_sessions[message.session]
            self.send_connected(self.ddp_session.ddp_session_id)
        else:
            session = Session()
            ddp_sessions[session.ddp_session_id] = session
            self.ddp_session = session
            self.send_connected(self.ddp_session.ddp_session_id)
    
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
        global ddp_subscriptions
        ddp_subscriptions.remove_id(message.id)

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
        self.write_message(message)
        for subscription_id in message.methods:
            ddp_subscriptions.remove_id(subscription_id)

    # Core Websockets Event Handlers
    def on_message(self, message):
        """
        DDP Deserialize the message and pass it on to the
        appropriate received message handler.
        """
        message = ddp.deserialize(message)
        ddp_session_id = None
        try:
            ddp_session_id = self.ddp_session.ddp_session_id
        except:
            pass
        #print "{} <<< {}".format(ddp_session_id, message)

        if self.ddp_session:
            self.ddp_session.set_expiry(90)

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

    def on_close(self):
        global ddp_subscriptions
        # Clean up subscriptions that belong to this session
        ddp_subscriptions.remove_session(self.ddp_session.ddp_session_id)
        # Destroy this session
        del self.ddp_session
        self.connections.remove(self)

    def check_origin(self, origin):
        """
        No security here. Just return true.
        """
        return True
