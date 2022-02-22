import socket
import select

HEADER_LEGTH = 10

IP = "127.0.0.1"
PORT= 1234

# Create a socket
# socket.AF_INET => address family, IPv4
# socket.SOCK_STREAM => TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# deal with server "Address already in use": reuse address
# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
server_socket.bind((IP, PORT))

# make server listen to new connections
server_socket.listen()

# list of sockets for select.select()
sockets_list = [server_socket]

# client dictionary. client_socket as key, user header and name as data
clients = {}

print(f"Listening for connections on {IP}:{PORT}...")


# Handle receiving a message
def receive_message(client_socket):
    try:

        # Recveive 'header' containing message length, it's size is defined and constant
        message_header = client_socket.recv(HEADER_LEGTH)
        
        # If we receive no data, client gracefully closed a connection, ex: using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False
        
        # Convert header into int value
        message_length = int(message_header.decode('utf-8').strip())
        
        # Return an obj of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # Something went wrong like empty message or client exited abruptly.
        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket i.e. a new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it is unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Client should send name right away, receive it
            user = receive_message(client_socket)

            # If False, client disconnected before sending name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save user name and user header
            clients[client_socket] = user

            print("Accepted new connection from {}:{}, username: {}".format(*client_address, user['data'].decode('utf-8')))
        
        # Else existing socket is sending a message
        else:

            # Receive a message
            message = receive_message(notified_socket)

            # If False the client disconnected, clean up socket list and clients
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, lets us know who sent the message
            user = clients[notified_socket]

            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            # Iterate over connected clients and broadcast message
            for client_socket in clients:

                # Don't send message to sender
                if client_socket != notified_socket:

                    # Send user and message (both with thier headers)
                    # Reusing message header sent by sender, and saved username header sent by user when first connected to server
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # In the event of socket exceptions, handle them
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from list of users
        del clients[notified_socket]                