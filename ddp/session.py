import uuid
import time

class Session(object):

    def __init__(self):
        self.ddp_session_id = self.gen_session_id()
        self.recs = {}
        self.expiry = time.time() + 90

    def gen_session_id(self):
        return str(uuid.uuid4())

    def has_rec(self, collection, id):
        return (collection,id) in self.recs.keys()

    def add_rec(self, collection, id, fieldnames=[]):
        if self.has_rec(collection, id):
            self.recs[(collection,id)] = list(set(self.recs[(collection,id)]).union(set(fieldnames)))
        else:
            self.recs[(collection,id)] = fieldnames

    def remove_rec(self, collection, id):
        del self.recs[(collection,id)]

    def set_expiry(self, secs):
        self.expiry = time.time() + secs

    def has_expired(self):
        if self.expiry == None:
            return False
        return self.expiry < time.time()

