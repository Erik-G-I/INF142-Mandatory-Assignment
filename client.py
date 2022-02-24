from socket import socket, AF_INET, SOCK_STREAM

socket = socket(AF_INET, SOCK_STREAM)

socket.connect(("localhost", 5555))