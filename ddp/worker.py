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
            message = self.queue.get()
            if message.msg in ['added', 'changed', 'removed']: 
                rec = (message.collection, message.id)
                for sub in self.subscriptions:
                    if not sub.has_rec(rec):
                        continue
                    sub.conn.write_message(message)


