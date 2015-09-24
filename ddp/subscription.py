class Subscription(object):
    """
    """

    def __init__(self, id, name, params, conn):
        self.id = id
        self.active = True
        self.recs = []
        self.conn = conn 
        self.name = name
        self.params = params

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

