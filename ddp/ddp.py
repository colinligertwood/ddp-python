import Queue
import ejson
from exceptions import NotImplementedError


class DDPError(Exception):
    """
    """

    def __init__(self, error, reason=None, details=None):
        self.error = error
        self.reason = reason
        self.details = details


class Message(object):
    """
    """

    msg = None
    _serialize_args = None

    def __init__(self, msg):
        """
        """
        self.msg = msg

    def ejson_serialize(self):
        """
        """
        message_dict = {'msg': self.msg}
        for arg in self._serialize_args:
            if arg == 'error' and not self.error:
                continue
            message_dict[arg] = self.__dict__.get(arg, None)
        return ejson.dumps(message_dict)

    def __repr__(self):
        value = super(Message, self).__repr__()
        return u"{} {}".format(value, self.ejson_serialize())

class Stop(Message):
    def __init__(self):
        super(Stop, self).__init__(u"stop")

class Connect(Message):
    _serialize_args = ("session", "version", "support")
    def __init__(self, session, version, support):
        """
        session: string (if trying to reconnect to an existing DDP session)
        version: string (the proposed protocol version)
        support: array of strings (protocol versions supported by the client, in order of preference)
        """
        super(Connect, self).__init__(u"connect")
        self.session = session
        self.version = version
        self.support = support


class Connected(Message):
    _serialize_args = ("session",)
    def __init__(self, session):
        """
        session: string (an identifier for the DDP session)
        """
        super(Connected, self).__init__(u"connected")
        self.session = session


class Failed(Message):
    _serialize_args = ("version",)
    def __init__(self, version='1'):
        """
        version: string (a suggested protocol version to connect with)
        """
        super(Failed, self).__init__(u"failed")
        self.version = version


class Ping(Message):
    _serialize_args = ("id",)
    def __init__(self, id=None):
        super(Ping, self).__init__(u"ping")
        self.id = id


class Pong(Message):
    _serialize_args = ("id",)
    def __init__(self, id=None):
        super(Pong, self).__init__(u"pong")
        self.id = id


class Sub(Message):
    _serialize_args = ("id", "name", "params")
    def __init__(self, id, name, params=None):
        """
        id: string (an arbitrary client-determined identifier for this subscription)
        name: string (the name of the subscription)
        params: optional array of EJSON items (parameters to the subscription)
        """
        super(Sub, self).__init__(u"sub")
        self.id = id
        self.name = name
        self.params = params


class UnSub(Message):
    _serialize_args = ("id",)
    def __init__(self, id):
        """
        id: string (the id passed to 'sub')
        """
        super(UnSub, self).__init__(u"unsub")
        self.id = id


class NoSub(Message):
    _serialize_args = ("id", "error")
    def __init__(self, id, error=None):
        """
        id: string (the id passed to 'sub')
        error: optional Error (an error raised by the subscription as it concludes, or sub-not-found)
        """
        super(NoSub, self).__init__(u"nosub")
        self.id = id
        self.error = error


class Added(Message):
    _serialize_args = ("collection", "id", "fields")
    def __init__(self, collection, id, fields=None):
       """
       collection: string (collection name)
       id: string (document ID)
       fields: optional object with EJSON values
       """
       super(Added, self).__init__(u"added")
       self.collection = collection
       self.id = id
       self.fields = fields


class Changed(Message):
    _serialize_args = ("collection", "id", "fields", "cleared")
    def __init__(self, collection, id, fields=None, cleared=None):
        """
        collection: string (collection name)
        id: string (document ID)
        fields: optional object with EJSON values
        cleared: optional array of strings (field names to delete)
        """
        super(Changed, self).__init__(u"changed")
        self.collection = collection
        self.id = id
        self.fields = fields
        self.cleared = cleared

class Removed(Message):
    _serialize_args = ("collection", "id")
    def __init__(self, collection, id):
        """
        collection: string (collection name)
        id: string (document ID)
        """
        super(Removed, self).__init__(u"removed")
        self.collection = collection
        self.id = id


class Ready(Message):
    _serialize_args = ("subs",)
    def __init__(self, subs):
        """
        subs: array of strings (ids passed to 'sub' which have sent their initial batch of data)
        """
        super(Ready, self).__init__(u"ready")
        self.subs = subs


class AddedBefore(Message):
    _serialize_args = ("collection", "id", "fields", "before")
    def __init__(self, collection, id, fields=None, before=None):
        """
        collection: string (collection name)
        id: string (document ID)
        fields: optional object with EJSON values
        before: string or null (the document ID to add the document before, or null to add at the end)
        """
        super(AddedBefore, self).__init__(u"addedBefore")
        self.collection = collection
        self.id = id
        self.fields = fields
        self.before = before


class MovedBefore(Message):
    _serialize_args = ("collection", "id", "before")
    def __init__(self, collection, id, before):
        """
        collection: string
        id: string (the document ID)
        before: string or null (the document ID to move the document before, or null to move to the end)
        """
        super(MovedBefore, self).__init__(u"movedBefore")
        self.collection = collection
        self.id = id
        self.before = before


class Method(Message):
    _serialize_args = ("method", "id", "params", "randomseed")
    def __init__(self, method, id, params=None, randomseed=None):
        """
        method: string (method name)
        params: optional array of EJSON items (parameters to the method)
        id: string (an arbitrary client-determined identifier for this method call)
        randomSeed: optional JSON value (an arbitrary client-determined seed for pseudo-random generators)
        """
        super(Method, self).__init__(u"method")
        self.method = method
        self.id = id
        self.params = params
        self.randomseed = randomseed


class Result(Message):
    _serialize_args = ("id", "error", "result")
    def __init__(self, id, error=None, result=None):
        """
        id: string (the id passed to 'method')
        error: optional Error (an error thrown by the method (or method-not-found)
        result: optional EJSON item (the return value of the method, if any)
        """
        super(Result, self).__init__(u"result")
        self.id = id

        # We're expecting an instance of DDPError which has a __dict__ attribute that's JSON serializable
        if error:
            self.error = error.__dict__
        else:
            self.error = None
        self.result = result


class Updated(Message):
    _serialize_args = ("methods",)
    def __init__(self, methods):
        """
        methods: array of strings (ids passed to 'method', all of whose writes have been reflected in data messages)
        """
        super(Updated, self).__init__(u"updated")
        self.methods = methods


msg_types = {
    'connect': Connect,
    'connected': Connected,
    'failed': Failed,
    'ping': Ping,
    'pong': Pong,
    'sub': Sub,
    'unsub': UnSub,
    'nosub': NoSub,
    'added': Added,
    'changed': Changed,
    'removed': Removed,
    'ready': Ready,
    'addedBefore': AddedBefore,
    'movedBefore': MovedBefore,
    'method': Method,
    'result': Result,
    'updated': Updated}


def serialize(msg_obj):
    return msg_obj.ejson_serialize()

def deserialize(msg_raw):
    msg = ejson.loads(msg_raw)
    msg_type = msg.get("msg", False)
    if not msg_type:
        raise Exception("No message type specified")
    if msg_type not in msg_types:
        raise Exception("Invalid message type")
    obj = msg_types[msg_type]
    return obj(*[msg.get(arg) for arg in obj._serialize_args])

