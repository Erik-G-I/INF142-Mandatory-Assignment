from multiprocessing import RLock
from socket import socket
from threading import Thread
from time import sleep
from champlistloader import load_some_champs
from core import pair_throw
import random
from core import Shape

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
    results = doRounds(3)
    print(results)
    print()
    printResults(results)



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
            # playerList.append(name)
            champ = champions.get(name)
            playerList.append(champ)
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

def doRound():
    results = []
    p1champindex = random.randint(0, 1)
    p2champindex = random.randint(0, 1)
    p1champ = player1[p1champindex]
    p2champ = player2[p2champindex]
    t1 = pair_throw(p1champ, p2champ)
    r1 = ((p1champ, p2champ), t1)

    p1champindex = updateIndex(p1champindex)
    p2champindex = updateIndex(p2champindex)
    p1champ = player1[p1champindex]
    p2champ = player2[p2champindex]
    t2 = pair_throw(p1champ, p2champ)
    r2 = ((p1champ, p2champ), t2)

    results.append(r1)
    results.append(r2)

    return results


def doRounds(amount):
    results = []
    for _ in range(amount):
        result = doRound()
        for throw in result:
            results.append(throw)

    return results

def updateIndex(index):
    index += 1
    if index > 1:
        index = 0
    return index

def printResults(result):
    blue_score = 0
    red_score = 0

    while len(result) > 0:
        round = result[0]
        champions = round[0]
        redChamp = champions[0]
        blueChamp = champions[1]
        pair = round[1]
        if pair.red > pair.blue:
            red_score += 1
        elif pair.red < pair.blue:
            blue_score += 1

        redChoice = emoji(pair.red.value)
        blueChoice = emoji(pair.blue.value)
        roundInfo = f'{redChamp.name} {redChoice}\n{blueChamp.name} {blueChoice}'
        sendToBothClients(roundInfo)



        

        print(f'{redChamp.name} {redChoice}')
        print(f'{blueChamp.name} {blueChoice}')


        print()

        result.pop(0)
    
    print(f'red score: {red_score}')
    print(f'blue score: {blue_score}')
    

def emoji(value):
    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }
    shape = None
    if value == 1:
        shape = Shape.ROCK
    elif value == 2:
        shape = Shape.PAPER
    elif value == 3:
        shape = Shape.SCISSORS
    
    return EMOJI.get(shape)
    
def sendToBothClients(message):
    message = message.encode()
    for conInfo in connections:
        connection = conInfo[0]
        connection.send(message)


accept(socket)