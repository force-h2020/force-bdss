import sys
import zmq

port = "5556"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:12345")
socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))
send_socket = context.socket(zmq.REQ)
send_socket.connect("tcp://localhost:12346")
send_socket.send("hello".encode("utf-8"))
while True:
    try:
        data = send_socket.recv_multipart(flags=zmq.NOBLOCK)
    except zmq.ZMQError:
        pass
    else:
        print("RECOVERING CACHE", data)
        break


while True:
    string = socket.recv()
    topic, messagedata = string.split()
    print(topic, messagedata)
