import socket
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    full_message = b""
    new_message = True
    while True:
        message = s.recv(16)
        if new_message:
            print("new message length:", message[:HEADERSIZE])
            message_length = int(message[:HEADERSIZE])
            new_message = False

        print(f"full message length: {message_length}")

        full_message += message

        print(len(full_message))

        if len(full_message)-HEADERSIZE == message_length:
            print("full message received")
            print(full_message[HEADERSIZE:])
            print(pickle.loads(full_message[HEADERSIZE:]))
            new_message = True
            full_message = b""
