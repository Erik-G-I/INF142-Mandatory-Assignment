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
    available_champs = socket.recv(1024).decode()
    if(available_champs.__sizeof__ == 0):
        break
    print(available_champs)
    

for _ in range(2):
    playerTurn = socket.recv(1).decode()
    if playerTurn == playerID:
        print("It is your turn")
        playerMove = input("Choose a champion: ")
        socket.send(playerMove.encode())

        moveLegality = socket.recv(1024).decode()
        while moveLegality != "True":
            print(moveLegality)
            playerMove = input("Choose a champion: ")
            socket.send(playerMove.encode())
            moveLegality = socket.recv(1024).decode()



for _ in range(6):
    result = socket.recv(512).decode()
    print(result)
input()