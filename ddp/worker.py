import threading
from globals import *

class Worker(threading.Thread):
    """
    """

    def __init__(self):
        self.active = True

    def start(self):
        global ddp_message_queue
        global ddp_subscriptions

        while self.active:
            message = ddp_message_queue.get()
            if message.msg in ['added']: 
                rec = (message.collection, message.id)
                for subscription in ddp_subscriptions:
                    if not subscription.has_rec(message.collection, message.id):
                        continue
                    subscription.conn.write_message(message)

            if message.msg in ['changed', 'removed']: 
                rec = (message.collection, message.id)
                for sub in ddp_subscriptions:
                    if not subscription.has_rec(message.collection, message.id):
                        continue
                    subscription.conn.write_message(message)

            if message.msg in ['ready']:
                for sub in ddp_subscriptions:
                    if not subscription.id in message.subs:
                        continue
                    subscription.conn.write_message(message)

            if message.msg in ['result']:
                for sub in ddp_subscriptions:
                    if not subscription.id in message.id:
                        continue
                    subscription.conn.write_message(message)

            if message.msg in ['updated']:
                for sub in ddp_subscriptions:
                    if not subscription.id in message.methods:
                        continue
                    subscription.conn.write_message(message)

