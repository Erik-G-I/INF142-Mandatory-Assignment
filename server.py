from socket import socket, AF_INET, SOCK_STREAM
from this import s
from threading import Thread
from core import pair_throw
from core import Shape
from core import Champion
import random
import json
from rich.table import Table
from datetime import datetime

def initialise_server():
    global socket
    socket = socket()
    socket.bind(("localhost", 5555))
    socket.listen()

def initialise_game():
    global connections
    global currentPlayer
    global player1
    global player2
    global champions
    global matchSummary
    connections = []
    currentPlayer = "2"
    player1 = []
    player2 = []
    champions = fetch_champs()
    matchSummary = ""


def fetch_champs():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 6000))
    initialCon = s.recv(128).decode()
    print(initialCon)

    request = "request_champ_data".encode()
    s.send(request)
    champions = s.recv(1024).decode()
    champions = json.loads(champions)
    s.close()

    print("Fetched the following champions from database:")
    for champ in champions:
        champ_stats = champions.get(champ)
        champion = convert_to_champ(champ_stats)
        champions[champ] = champion
        print(champion)
        
    return champions

def convert_to_champ(champ_stats):
    name = champ_stats[0]
    rock = champ_stats[1]
    paper = champ_stats[2]
    scissors = champ_stats[3]

    return Champion(name, rock, paper, scissors)


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
        print("Waiting for client(s)...")
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
    global champions
    global player1
    global player2
    
    match playerMove:
        case name if name not in champions:
            return (False, f'The champion is not available. Try again.')

        case name if champions.get(name) in playerList:
            return (False, f'{name} is already in your team. Try again.')
            
        case name if champions.get(name) in player1:
            return (False, f'{name} is in the enemy team. Try again.')
                
        case name if champions.get(name) in player2:
            return (False, f'{name} is in the enemy team. Try again.')
                
        case _:
            champ = champions.get(name)
            playerList.append(champ)
            return (True, "")


def print_available_champs(champions, connection):
    table_string = ""
    for champion in champions.values():
        if champion not in player1 and champion not in player2:
            table_string += f'{champion}\n'
    connection.send(table_string.encode())


def doPlayerTurn(connection, playerID):
    print_available_champs(champions, connection)
    playerTurn = updatePlayer()
    connection.send(playerTurn.encode())
    
    if str(playerID) == playerTurn:
        while True:
            playerMove = connection.recv(64).decode()
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
    global matchSummary
    blue_score = 0
    red_score = 0
    gameInfo = ""
    roundNum = 1
    while len(result) > 0:
        roundInfo = ''
        roundNum+=1
        round = result[0]
        champions = round[0]
        redChamp = champions[0]
        blueChamp = champions[1]
        pair = round[1]
        if pair.red > pair.blue:
            red_score += 1
        elif pair.red < pair.blue:
            blue_score += 1

        if roundNum%2 == 0:
            roundInfo += f'Round {"{:.0f}".format(roundNum/2)}\n'
        redChoice = emoji(pair.red.value)
        blueChoice = emoji(pair.blue.value)
        roundInfo += f'[red]{redChamp.name}[/red] {redChoice}\n[blue]{blueChamp.name}[/blue] {blueChoice}\n\n'
        gameInfo += roundInfo
        result.pop(0)
    
    if red_score == blue_score:
        winner = "Draw, GGWP"
    elif red_score > blue_score:
        winner = "[red]Red[/red] wins!"
    else:
        winner = "[blue]Blue[/blue] wins!"
    
    red_score = f'[red]red score[/red]: {red_score}'
    blue_score = f'[blue]blue score[/blue]: {blue_score}'
    gameInfo += red_score + '\n' + blue_score + '\n' + winner
    
    print(gameInfo)
    sendToBothClients(gameInfo)
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    matchSummary = timestamp + '\n' + gameInfo
    

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

def writeMatchDetails(message):
    message = message.encode()
    db = socket(AF_INET, SOCK_STREAM)
    db.connect(("localhost", 6000))
    initialCon = db.recv(128).decode()
    print(initialCon)

    db.send("write match details".encode())
    db.recv(1024).decode()
    db.send(message)
    db.close()


initialise_game()
initialise_server()
accept(socket)
writeMatchDetails(matchSummary)