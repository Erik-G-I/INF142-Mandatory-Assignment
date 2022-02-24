from socket import socket

socket = socket()

socket.bind(("", 5555))
socket.listen()
connectedClients = []

while len(connectedClients) < 2:
    connection, addr = socket.accept()
    connectedClients.append((connection, addr))

while True:

    print("Got connection from: ", connectedClients[0])
    print("Got connection from: ", connectedClients[1])
    connectedClients[0][0].send("poop".encode())
    connectedClients[1][0].send("poop".encode())


    break