from socket import socket

socket = socket()

socket.bind(("", 5555))
socket.listen()

connection, addr = socket.accept()

while True:
    print("Got connection from: ", addr)
    break