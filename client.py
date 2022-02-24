from socket import socket, AF_INET, SOCK_STREAM

socket = socket(AF_INET, SOCK_STREAM)

socket.connect(("localhost", 5555))

test = socket.recv(1024).decode()
print(test)
input("")

