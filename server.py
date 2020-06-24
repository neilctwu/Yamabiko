import socket
import sys
import time

host = 'localhost'
port = 8220
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen()

print("Listening for client . . .")
conn, address = server_socket.accept()
print("Connected to client at ", address)
#pick a large output buffer size because i dont necessarily know how big the incoming packet is
while True:
    output = conn.recv(2048)
    if output.strip() == "disconnect".encode():
        conn.close()
        sys.exit("Received disconnect message.  Shutting down.")
    elif output:
        print("Message received from client:")
        print(output)
        conn.send("a".encode())
        time.sleep(5)
        conn.send("ack".encode())