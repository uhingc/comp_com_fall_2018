
# Quincy Chatroom Server
from socket import *
from thread import *

#add 20 to each ascii value for rudimentary encryption
def encrypt(message):
    asc = [ord(c) for c in message]
    asc_to_send = [x+20 for x in asc]
    str_to_send = ''.join(chr(i) for i in asc_to_send)
    return str_to_send

#subtract 20 to each ascii value for rudimentary decryption
def decrypt(message):
    junk_asc = [ord(c) for c in message]
    good_asc = [x-20 for x in junk_asc]
    good_str = ''.join(chr(i) for i in good_asc)
    return good_str


# Define Server IP address
ip_address = '192.168.247.1'

# Define Software Port [agreed point of communication]
port = 12345

# Create Server Socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Bind socket to IP address
server_socket.bind((ip_address, port));

# Enable server to accept connections
server_socket.listen(5)

# List of client connections
client_connections = []

# Server Up and Running Message
print "Server up and Running!"

# Thread to Handle Send and Receiver for Client and Server
def new_client_thread(connection_socket, client_address):
   
    # Welcome Message
    connection_socket.send(encrypt("Welcome to the chatroom"))

    while True:
        # Server listens for client message    
        message = connection_socket.recv(1024)
		message = decrypt(message)
        message = message.replace('\r', '').replace('\n', '')
		
        # Check for exit command
        if message == "EXIT":		
            exit_message = "[Client Left Chatroom] " + client_address[0]
			
            # Exit Message to Server Terminal
            print exit_message
			
			# Remove client from list of client connections
            client_connections.remove(client)
			
            # Exit Message to All Cients
            for client in client_connections:
                client.send(decrypt(exit_message))
			
            # close socket
            connection_socket.close

            # exit thread
            exit()

        # Display Message
        client_message = "<" + client_address[0] + "> " + message
        print client_message

        # Broadcast message to all clients
        for client in client_connections:
            try:
                client.send(encrypt(client_message))
            except:
                client.close()
                client_connections.remove(client)
                #exit()


# Listen and Serve Messages
while True:
    # Accept a new connection on socket
    connection_socket, client_address = server_socket.accept()
 
    # Display New Client Connection on Server
    print "[Client Entered Chatroom] " + client_address[0]


    # Add new clients to client list
    client_connections.append(connection_socket)


    # Start Thread For Client
    start_new_thread(new_client_thread,(connection_socket,client_address))

    







