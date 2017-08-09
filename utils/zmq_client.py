import sys
import zmq

port = "5556"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect ("tcp://localhost:12345")

socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))

while True:
    string = socket.recv()
    topic, messagedata = string.split()
    print(topic, messagedata)
