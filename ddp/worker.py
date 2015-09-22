import threading

class Worker(threading.Thread):
    """
    """

    def __init__(self, queue, subscriptions):
        self.queue = queue
        self.subscriptions = subscriptions
        self.active = True

    def start(self):
        while self.active:
            message = self.queue.get()
            if message.msg not in ['added', 'changed', 'removed', 'ready', 'result']:
                continue
           
            if message.msg in ['added', 'changed', 'removed']: 
                rec = (message.collection, message.id)
                for sub in self.subscriptions:
                    if not sub.has_rec(rec):
                        continue
                    sub.conn.write_message(message)


