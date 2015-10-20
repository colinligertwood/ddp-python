class Subscription(object):
    """
    """

    def __init__(self, id, name, params, conn, method=False):
        self.id = id
        self.active = True
        self.conn = conn 
        self.name = name
        self.params = params
        self.method = method

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def on_added(self, message):
        self.conn.ddp_session.add_rec(message.collection, message.id, message.fields.keys())
        self.conn.write_message(message)

    def on_changed(self, message):
        if self.conn.ddp_session.has_rec(message.collection, message.id):
            self.conn.write_message(message)

    def on_removed(self, message):
        if self.conn.ddp_session.has_rec(message.collection, message.id):
            self.conn.ddp_session.remove_rec(message.collection, message.id)
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
            self.method = 'reapme'



