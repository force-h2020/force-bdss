import zmq

# Socket to talk to server
context = zmq.Context()
sub_socket = context.socket(zmq.SUB)
sub_socket.bind("tcp://*:12345")
sub_socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))
sub_socket.setsockopt(zmq.LINGER, 0)

sync_socket = context.socket(zmq.REP)
sync_socket.setsockopt(zmq.LINGER, 0)
sync_socket.bind("tcp://*:12346")

poller = zmq.Poller()
poller.register(sub_socket)
poller.register(sync_socket)

WAITING = 0
RECEIVING = 1

state = WAITING

while True:
    events = dict(poller.poll())
    if sync_socket in events:
        data = sync_socket.recv_string()
        print("received ", data)
        if data == "HELLO 1":
            sync_socket.send_string("HELLO 1")
            state = RECEIVING
        elif data == "GOODBYE 1":
            sync_socket.send_string("GOODBYE 1")
            state = WAITING
        else:
            print("unknown request", data)

    if sub_socket in events:
        if state == RECEIVING:
            string = sub_socket.recv_string()
            split_data = string.split("\n")
            print(split_data)
        else:
            print("data while waiting. discarding")
            string = sub_socket.recv_string()
