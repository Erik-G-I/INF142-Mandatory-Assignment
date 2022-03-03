from socket import socket
from threading import Thread
import threading
from time import sleep

socket = socket()

socket.bind(("", 5555))
socket.listen()
connections = []
currentPlayer = "2"

def updatePlayer():
    global currentPlayer
    if currentPlayer == "1":
        currentPlayer = "2"
    elif currentPlayer == "2":
        currentPlayer = "1"
    else:
        raise Exception("PlayerID must be 1 or 2")
    return currentPlayer

# code from slides, Lecture 7
def accept(socket):
    while len(connections) < 2:
        connection, addr = socket.accept()
        print("Accepted", connection, "from", addr)
        playerID = str(len(connections)+1)
        connections.append((connection, playerID))
        connection.send("Successfully connected".encode())
        connection.send(playerID.encode())

    doTurns(2)

def isLegal(playerMove):
    # This function is supposed to see if a given player move is accepted by the game
    return True

def doTurn(connection, playerID):
    playerTurn = updatePlayer()
    connection.send(playerTurn.encode())
    
    if str(playerID) == playerTurn:
        while True:
            playerMove = connection.recv(1024)
            if isLegal(playerMove):
                connection.send("True".encode())
            else:
                connection.send("False".encode())

    print(f"Player {playerID} chose {playerMove}")


def turnSetup():
    for conInfo in connections:
        connection = conInfo[0]
        playerID = conInfo[1]
        thread = Thread(target=doTurn, args=(connection, playerID,))
        thread.start()
        thread.join()


def doTurns(amount):
    for _ in range(amount):
        turnSetup()

    


    





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