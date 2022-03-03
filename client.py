from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 5555))

initialCon = socket.recv(1024).decode()
print(initialCon)


playerID = socket.recv(1).decode()
print(f"You are Player {playerID}")
print()


while True:
    playerTurn = socket.recv(1).decode()
    if playerTurn == playerID:
        print("It is your turn")
        playerMove = input("Choose a champion: ")
        socket.send(playerMove.encode())

        moveLegality = socket.recv(1024)
        while moveLegality == "False":
            print("Illegal move")
            playerMove = input("Choose a champion: ")
            socket.send(playerMove.encode())
            moveLegality = socket.recv(1024)