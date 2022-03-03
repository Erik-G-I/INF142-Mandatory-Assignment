from socket import socket
from threading import Thread
from time import sleep
from champlistloader import load_some_champs

socket = socket()

socket.bind(("", 5555))
socket.listen()
connections = []
currentPlayer = "2"
player1 = []
player2 = []
champions = load_some_champs()

def updatePlayer():
    global currentPlayer
    if currentPlayer == "1":
        currentPlayer = "2"
    elif currentPlayer == "2":
        currentPlayer = "1"
    else:
        raise Exception("PlayerID must be 1 or 2")
    return currentPlayer


def accept(socket):
    while len(connections) < 2:
        connection, addr = socket.accept()
        print("Accepted", connection, "from", addr)
        playerID = str(len(connections)+1)
        connections.append((connection, playerID))
        connection.send("Successfully connected".encode())
        connection.send(playerID.encode())

    doTurns(2)


def choosePlayerList(playerID, playerMove):
    if playerID == "1":
        return isLegal(playerMove, player1)
    if playerID == "2":
        return isLegal(playerMove, player2)
    else:
        raise Exception("Invalid playerID")

def isLegal(playerMove, playerList):
    # This function is supposed to see if a given player move is accepted by the game
    # Fix this at some point
    global champions
    global player1
    global player2

    match playerMove:
        case name if name not in champions:
            return (False, f'The champion {name} is not available. Try again.')

        case name if name in playerList:
            return (False, f'{name} is already in your team. Try again.')
            
        case name if name in player1:
            return (False, f'{name} is in the enemy team. Try again.')
                
        case name if name in player2:
            return (False, f'{name} is in the enemy team. Try again.')
                
        case _:
            playerList.append(name)
            return (True, "")
    


def doPlayerTurn(connection, playerID):
    playerTurn = updatePlayer()
    connection.send(playerTurn.encode())
    
    if str(playerID) == playerTurn:
        while True:
            playerMove = connection.recv(1024).decode()
            moveLegality = choosePlayerList(playerID, playerMove)
            if moveLegality[0]:
                connection.send("True".encode())
                break
            else:
                connection.send(moveLegality[1].encode())
    
    print(f"Player {playerID} chose {playerMove}")


def turnSetup():
    for conInfo in connections:
        connection = conInfo[0]
        playerID = conInfo[1]
        thread = Thread(target=doPlayerTurn, args=(connection, playerID,))
        thread.start()
        thread.join()


def doTurns(amount):
    for _ in range(amount):
        turnSetup()


accept(socket)