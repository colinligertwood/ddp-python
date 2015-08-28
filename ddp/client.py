import websocket
import ddp

if __name__ == "__main__":
    ws = websocket.create_connection("ws://localhost:9980/ws")
    connect_obj = ddp.Connect("MySession", "1", [1])
    ws.send(ddp.serialize(connect_obj))
    print ddp.deserialize(ws.recv())
    ping_obj = ddp.Ping("MyId")
    ws.send(ddp.serialize(ping_obj))
    print ddp.deserialize(ws.recv())
    sub_obj = ddp.Sub("1", "product.product", ["[('default_code', 'ilike', 'T-LSM%')]"])
    ws.send(ddp.serialize(sub_obj))
    print ddp.deserialize(ws.recv())
