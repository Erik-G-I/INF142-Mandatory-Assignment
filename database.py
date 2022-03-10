from socket import socket, AF_INET, SOCK_STREAM
import json

socket = socket(AF_INET, SOCK_STREAM)
socket.bind(("localhost", 6000))
socket.listen()


def from_csv(filename: str) -> dict[str, tuple]:
    champions = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            name, rock, paper, scissors = line.split(sep=',')
            champions[name] = (name, float(rock), float(paper), float(scissors))
    return champions

def load_some_champs():
    return from_csv('some_champs.txt')

    
def accept(socket):
    while True:
        print("Listening...")
        connection, addr = socket.accept()
        connection.send("Successfully connected to database".encode())
        request = connection.recv(1024).decode()
        print(request)
        handle_request(request, connection)



def handle_request(request, connection):
    if request == "request_champ_data":
        champions = load_some_champs()
        champions = json.dumps(champions)
        print()
        print(f"Sending the following to {connection}:\n")
        print(champions)
        print()
        connection.send(str(champions).encode())


accept(socket)