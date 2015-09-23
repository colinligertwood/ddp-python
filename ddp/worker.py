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
        print ddp_message_queue, ddp_subscriptions

        while self.active:
            print ddp_message_queue, ddp_subscriptions
            message = ddp_message_queue.get()
            if message.msg in ['added', 'changed', 'removed']: 
                rec = (message.collection, message.id)
                for sub in ddp_subscriptions:
                    if not sub.has_rec(message.collection, message.id):
                        continue
                    sub.conn.write_message(message)

            if message.msg in ['ready']:
                for sub in ddp_subscriptions:
                    if not sub.id in message.subs:
                        continue
                    sub.conn.write_message(message)

