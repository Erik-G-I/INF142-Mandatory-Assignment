from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from rich import print

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 5555))

initialCon = socket.recv(1024).decode()
print(initialCon)

playerID = socket.recv(1).decode()
number_of_champs = 0
print(f"You are Player {playerID}")
print()

for _ in range(2): # Game loop

    # Available champions
    champs = socket.recv(1024).decode()
    print(champs)

    # Move choice stuff
    playerTurn = socket.recv(1).decode()
    if playerTurn == playerID:
        print("It is your turn")
        playerMove = input("Choose a champion: ")
        socket.send(playerMove.encode())

        moveLegality = socket.recv(64).decode()
        while moveLegality != "True":
            print(moveLegality)
            playerMove = input("Choose a champion: ")
            socket.send(playerMove.encode())
            moveLegality = socket.recv(64).decode()



print()
result = socket.recv(1024).decode()
print(result)

input()