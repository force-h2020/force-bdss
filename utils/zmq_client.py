import zmq

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:12345")
socket.setsockopt(zmq.SUBSCRIBE, "".encode("utf-8"))
send_socket = context.socket(zmq.REQ)
send_socket.connect("tcp://localhost:12346")

send_socket.send("SYNC".encode("utf-8"))
data = send_socket.recv_multipart()
for d in data:
    split_data = d.split()
    print("SYNCED ", split_data)

while True:
    string = socket.recv()
    split_data = string.split()
    print(split_data)
