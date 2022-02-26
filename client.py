from socket import socket, AF_INET, SOCK_STREAM
from time import sleep

socket = socket(AF_INET, SOCK_STREAM)
socket.connect(("localhost", 5555))

initialCon = socket.recv(1024).decode()
print(initialCon)


playerID = socket.recv(1).decode()
print(f"You are Player {playerID}")
print()


playerTurn = socket.recv(1).decode()
if playerTurn == playerID:
    print("It is your turn")
    input("Choose a champion: ")
else:
    print("It is your opponent's turn")


input()