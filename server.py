import imp
from socket import socket
from threading import Thread

socket = socket()

socket.bind(("", 5555))
socket.listen()
connectedClients = []

# code from slides, Lecture 7
def accept(socket):
    while True:
        connection, addr = socket.accept()
        print("Accepted", connection, "from", addr)
        Thread(target=read, args=(connection)).start()

def read(connection):
    while True:
        data = connection.recv(1024)
        if data:
            sentence = data.decode()
            new_sentence = sentence.upper()
            connection.send(new_sentence.encode())
        else:
            print('closing', connection)
            connection.close()
            break

while len(connectedClients) < 2:
    connection, addr = socket.accept()
    connectedClients.append((connection, addr))

while True:

    print("Got connection from: ", connectedClients[0])
    print("Got connection from: ", connectedClients[1])
    connectedClients[0][0].send("poop".encode())
    connectedClients[1][0].send("poop".encode())


    break