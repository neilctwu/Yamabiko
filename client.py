import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8220))

for index in range(5):
    data = "GET\nSONAR%d\n\n" % index
    print('send to server: ' + data)
    client_socket.send(data.encode())
    while client_socket.recv(2048) != "ack".encode():
        print("waiting for ack")
    print( "ack received!")

#send disconnect message
dmsg = "disconnect"
print("Disconnecting")
client_socket.send(dmsg.encode())

client_socket.close()