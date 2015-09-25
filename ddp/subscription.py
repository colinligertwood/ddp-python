class Subscription(object):
    """
    """

    def __init__(self, id, name, params, conn, method=False):
        self.id = id
        self.active = True
        self.recs = []
        self.conn = conn 
        self.name = name
        self.params = params
        self.method = method

    def has_rec(self, collection, id):
        return (collection,id) in self.recs

    def add_rec(self, collection, id):
        self.recs.append((collection,id))

    def remove_rec(self, collection, id):
        self.recs.remove((collection,id))

    def reset(self):
        self.recs = []

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def on_added(self, message):
        if not self.has_rec(message.collection, message.id):
            self.add_rec(message.collection, message.id)
        self.conn.write_message(message)

    def on_changed(self, message):
        if self.has_rec(message.collection, message.id):
            self.conn.write_message(message)

    def on_removed(self, message):
        if self.has_rec(message.collection, message.id):
            self.conn.write_message(message)

    def on_ready(self, message):
        if self.id in message.subs:
            self.conn.write_message(message)

    def on_result(self, message):
        if self.id in message.id:
            self.conn.write_message(message)

    def on_updated(self, message):
        if self.id in message.methods:
            self.conn.write_message(message)

