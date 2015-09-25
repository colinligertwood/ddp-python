import websocket
import ddp
import sys

class Client(object):
    def __init__(self, url):
        self.url = url
        self.ws = websocket.create_connection(url)

    def send(self, message):
        self.ws.send(ddp.serialize(message))
    
    def recv(self):
        return ddp.deserialize(self.ws.recv())

    def send_recv(self, message):
        self.send(message)
        return self.recv()

    def connect(self, session=None, protocol="1"):
        self.protocol = protocol
        return self.send_recv(ddp.Connect(session, protocol, [protocol]))

if __name__ == "__main__":
    client = Client("ws://localhost")
    print client.connect()

    # Send a ping
    print client.send_recv(ddp.Ping("yummy"))

