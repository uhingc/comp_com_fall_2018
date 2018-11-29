
# Quincy Chatroom Client
from socket import *
from select import *
import sys
import time

# Define Server IP address
ip_address = '192.168.247.1'

# Define Software Port [agreed point of communication]
port = 12345

# Create Client Socket
server_socket = socket(AF_INET, SOCK_STREAM)

# Connect to Server [using server IP address and agreed upon port number]
server_socket.connect((ip_address, port))


# Send or Receive Message
while True:
    selectable_object_list = [sys.stdin, server_socket]
    
    # Poll socket for ready flag
    read_ready,_,_ = select(selectable_object_list,[],[])    


    # Receive Message From Server
    if read_ready[0] == server_socket:
        message = server_socket.recv(1024)
        message = message.replace('\r', '').replace('\n', '')        
        print message

		
    # Client Message to Server
    if read_ready[0] == sys.stdin:
        message = sys.stdin.readline()
        message = message.replace('\r', '').replace('\n', '')
		
        server_socket.send(message)
        sys.stdout.flush()
		
		# Check for EXIT Message
        if message == "EXIT":	
            print "Exiting chatroom"
            exit()

# Close Socket Connection
client_socket.close()

