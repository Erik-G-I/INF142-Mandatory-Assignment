from socket import socket
from threading import Thread
import threading
from time import sleep

socket = socket()

socket.bind(("", 5555))
socket.listen()
threads = []

# code from slides, Lecture 7
def accept(socket):
    while True:
        connection, addr = socket.accept()
        print("Accepted", connection, "from", addr)
        thread = Thread(target=read, args=(connection,))
        threads.append(thread)
        thread.start()

def read(connection):
    connection.send(str.encode("Connected"))
    playerID = str(len(threads)).encode()
    connection.send(playerID)
    
    while len(threads) < 2:
        continue

    while True:
        playerTurn = "1"
        connection.send(playerTurn.encode())



        # data = connection.recv(1024)
        # if data:
        #     sentence = data.decode()
        #     new_sentence = sentence.upper()
        #     connection.send(new_sentence.encode())
        # else:
        #     print('closing', connection)
        #     connection.close()
        #     break


accept(socket)