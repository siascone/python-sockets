import socket
import time
import pickle

HEADERSIZE = 10

# create the socket
# AF_INT == ipv4
# SOCK_STREAM == TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.shutdown(socket.SHUT_RDWR)
# s.close()

# bind socket to server port
s.bind((socket.gethostname(), 1234))

# conneciton queue
s.listen(5)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    d = {1: "hi", 2: "there"}
    message = pickle.dumps(d)
    message = bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message
    print(message)
    clientsocket.send(message)

    # message = "Welcome to the server"
    # message = f"{len(message):<{HEADERSIZE}} + message"

    # clientsocket.send(bytes(message, "utf-8"))
    # clientsocket.close()

    # while True:
    #     time.sleep(3)
    #     message = f"The time is {time.time()}"
    #     message = f"{len(message):<{HEADERSIZE}}" + message

    #     print(message)

    #     clientsocket.send(bytes(message, "utf-8"))