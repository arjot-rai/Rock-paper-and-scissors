import socket
from _thread import *
import pickle
from game import *

server = "172.16.1.67"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
currentP = 0

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(2)

print("Server Started\nWaiting for connections...")

def threaded_client(conn, player, gameID):
    conn.send(str(player).encode())
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameID in games:
                if not data:
                    print("Disconnected")
                    break
                else:
                    if data == "reset":
                        games[gameID].reset()
                    elif data == "disconnect":
                        games[gameID].quit = True
                    elif data != "get":
                        games[gameID].play(player, data)

                reply = games[gameID]

                conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    conn.close()

games = {}
count = 0
while True:
    conn, address = s.accept()
    print("Connected to: ", address)
    currentP = 0
    count += 1
    gameID = (count - 1)//2

    if count % 2 == 1:
        games[gameID] = Game(gameID)
    else:
        games[gameID].bothReady = True
        currentP = 1

    start_new_thread(threaded_client, (conn, currentP, gameID))
