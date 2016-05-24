import threading
from ddp import Stop
from globals import *

class Worker(object):
    """
    """

    def __init__(self):
        self.active = True

    def start(self):
        global ddp_message_queue
        global ddp_subscriptions

        while self.active:
            (message) = ddp_message_queue.dequeue()
            for subscription in ddp_subscriptions:
                if message.msg == 'added':
                    subscription.on_added(message)

                elif message.msg == 'changed':
                    subscription.on_changed(message) 

                elif message.msg == 'removed':
                    subscription.on_removed(message)

                elif message.msg == 'ready':
                    subscription.on_ready(message)

                elif message.msg == 'result':
                    subscription.on_result(message)

                elif message.msg == 'updated':
                    subscription.on_updated(message)

    def stop(self):
        global ddp_message_queue
        ddp_message_queue.enqueue(Stop())
        self.active = False

