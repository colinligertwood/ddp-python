import threading
from globals import *

class Worker(threading.Thread):
    """
    """

    def __init__(self):
        self.active = True

    def on_added(self, subscription, message):
        if not subscription.has_rec(message.collection, message.id):
            subscription.add_rec(message.collection, message.id)
        subscription.conn.write_message(message)

    def on_changed(self, subscription, message):
        if subscription.has_rec(message.collection, message.id):
            subscription.conn.write_message(message)

    def on_removed(self, subscription, message):
        self.on_changed(subscription, message)

    def on_ready(self, subscription, message):
        if subscription.id in message.subs:
            subscription.conn.write_message(message)

    def on_result(self, subscription, message):
        if subscription.id in message.id:
            subscription.conn.write_message(message)

    def on_updated(self, subscription, message):
        if subscription.id in message.methods:
            subscription.conn.write_message(message)

    def start(self):
        global ddp_message_queue
        global ddp_subscriptions

        while self.active:
            message = ddp_message_queue.get()
            for subscription in ddp_subscriptions:
                if message.msg == 'added':
                    self.on_added(subscription, message)

                elif message.msg == 'changed':
                    self.on_changed(subscription, message) 

                elif message.msg == 'removed':
                    self.on_removed(subscription, message)

                elif message.msg == 'ready':
                    self.on_ready(subscription, message)

                elif message.msg == 'result':
                    self.on_result(subscription, message)

                elif message.msg in ['updated']:
                    self.on_updated(subscription, message)

